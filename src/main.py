
import json
import os
from pathlib import Path


from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from agents.factory import factory
from agents.factory.factory import AgentFactory
from agents.system.fallback_agent import FallbackAgent
from agents.domain.finance_agent import FinanceAgent
from agents.domain.hr_agent import HRAgent
from agents.system.orchestrator import Orchestrator
from agents.domain.tech_agent import TechAgent
from agents.system.evaluator_agent import EvaluatorAgent
from rag.pipeline import RAGPipeline
from routing.keyword_router import  KeywordRouter
from shared.config_loader import ConfigLoader
from shared.logger import get_logger
from shared.tracer import Tracer

ROOT_DIR = Path(__file__).parent.parent

load_dotenv()

# Carga la configuración
config = ConfigLoader()
log = get_logger("main")

llm = ChatOpenAI(
    model=config.get("llm.model"),
    temperature=config.get("llm.temperature"),
    max_tokens=config.get("llm.max_tokens"),
)

embeddings = OpenAIEmbeddings()


def main():
    print("=" * 50)
    log.info("  TECHFLOW - SISTEMA MULTIAGENTE")
    print("=" * 50)

   
    factory = AgentFactory(config, embeddings, llm)
    agents = factory.create_agents()
    agents["unknown"] = FallbackAgent()
    
    log.info(f"Agentes creados.")
    router = KeywordRouter(fallback_domain=config.get("routing.fallback_domain", "unknown"))
    log.info(f"Router creado.")
    tracer = Tracer()
    log.info(f"Tracer creado.")
    orchestrator = Orchestrator(router=router, agents=agents, tracer=tracer)
    log.info(f"Orchestrator creado.")
    evaluator    = EvaluatorAgent(llm=llm)
    log.info(f"Evaluador creado.")
    log.info(f"Sistema listo.\n")
 
    # Ejecutamos las consultas de prueba
    try:
        with open(ROOT_DIR / "test_queries.json", "r", encoding="utf-8") as f:
            test_queries = json.load(f)
    except Exception as e:
        log.error(f"No se pudieron cargar las queries: {e}")
        return

    results = []
    for item in test_queries:
        # empieza tracer
        with tracer.start_trace(
            name="m3-multi-agent",
            input_data={"question":  item["query"]}
        ) as trace:
            try:
                trace_id = trace.id
                query = item["query"]
                expected = item["expected_domain"]

                result = orchestrator.route(query)

                evaluation = evaluator.evaluate(
                    query=query,
                    answer=result["answer"],
                )

                final_score = sum([
                    evaluation["relevance"],
                    evaluation["accuracy"],
                    evaluation["completeness"]
                ]) / 3

                tracer.add_score(
                    trace_id=trace_id,
                    name="overall",
                    value=final_score,
                    comment=evaluation["reasoning"]
                )

                match = "✓" if result["domain"] == expected else "✗"

                log.info(f"{match} Dominio detectado: {result['domain']} | Esperado: {expected}")
                log.info(f"Evaluación: {evaluation}")
                print("=" * 50)
                results.append({
                    **result,
                    "expected_domain": expected,
                    "evaluation": evaluation
                })

            except Exception as e:
                log.error(f"Error procesando query '{item.get('query')}': {e}")

                results.append({
                    "query": item.get("query"),
                    "error": str(e)
                })
 
    # Guardamos resultados
    try:
        (ROOT_DIR / "outputs").mkdir(exist_ok=True)

        with open(ROOT_DIR / "outputs" / "test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    except Exception as e:
        log.error(f"No se pudieron guardar los resultados: {e}")
    

    tracer.flush()
    log.info("\n✓ Resultados guardados en outputs/test_results.json")
 


if __name__ == "__main__":
    main()
