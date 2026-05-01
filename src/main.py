
import json
import os
from pathlib import Path


from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from agents.finance_agent import FinanceAgent
from agents.hr_agent import HRAgent
from agents.orchestrator import Orchestrator
from agents.tech_agent import TechAgent
from agents.evaluator_agent import EvaluatorAgent
from rag.pipeline import RAGPipeline
from routing.keyword_router import  KeywordRouter
from shared.config_loader import ConfigLoader
from shared.tracer import Tracer

ROOT_DIR = Path(__file__).parent.parent

load_dotenv()

# Carga la configuración
config = ConfigLoader()

llm = ChatOpenAI(
    model=config.get("llm.model"),
    temperature=config.get("llm.temperature"),
    max_tokens=config.get("llm.max_tokens"),
)

embeddings = OpenAIEmbeddings()

def create_agents():
    """Crea los agentes para cada dominio usando RAGPipeline."""
    agents = {}
    for domain in ["hr", "tech", "finance"]:
        pipeline = RAGPipeline(domain=domain, config=config)
        retriever = pipeline.build(embeddings=embeddings)

        if domain == "hr":
            agents[domain] = HRAgent(retriever=retriever, llm=llm)
        elif domain == "tech":
            agents[domain] = TechAgent(retriever=retriever, llm=llm)
        elif domain == "finance":
            agents[domain] = FinanceAgent(retriever=retriever, llm=llm)

    return agents

def main():
    print("=" * 50)
    print("  TECHFLOW - SISTEMA MULTIAGENTE")
    print("=" * 50)

   
    agents = create_agents()
    print(f"Agentes creados.")
    router = KeywordRouter(fallback_domain=config.get("routing.fallback_domain", "hr"))
    print(f"Router creado.")
    tracer = Tracer()
    print(f"Tracer creado.")
    orchestrator = Orchestrator(router=router, agents=agents, tracer=tracer)
    print(f"Orchestrator creado.")
    evaluator    = EvaluatorAgent(llm=llm)
    print(f"Evaluador creado.")
    print(f"\nSistema listo.\n")
 
    # Ejecutamos las consultas de prueba
    with open(ROOT_DIR / "test_queries.json", "r", encoding="utf-8") as f:
        test_queries = json.load(f)

    results = []
    for item in test_queries:
        # empieza tracer
        with tracer.start_trace(
            name="m3-multi-agent",
            input_data={"question":  item["query"]}
        ) as trace:
            trace_id = trace.id
            query    = item["query"]
            expected = item["expected_domain"]
    
            # 1. Ejecutamos la consulta
            result = orchestrator.route(query)
            match  = "✓" if result["domain"] == expected else "✗"

            # 2. Evaluamos la respuesta
            evaluation = evaluator.evaluate(
                query=query,
                answer=result["answer"],
            )

            tracer.add_score(
                trace_id=trace_id,
                name="overall",
                value=sum([
                    evaluation["relevance"],
                    evaluation["accuracy"],
                    evaluation["completeness"]
                ]) / 3,
                comment=evaluation["reasoning"]
            )
    
            # 4. Mostramos en terminal
            print(f"{match} Dominio detectado: {result['domain']} | Esperado: {expected}")
            print(f"   Evaluación: relevance: {evaluation['relevance']}/10, accuracy: {evaluation['accuracy']}/10, completeness: {evaluation['completeness']}/10 — {evaluation['reasoning']}")
            print("=" * 60)

            results.append({**result, "expected_domain": expected, "evaluation": evaluation})
 
    # Guardamos resultados
    (ROOT_DIR / "outputs").mkdir(exist_ok=True)
    with open(ROOT_DIR / "outputs" / "test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
 

    tracer.flush()
    print("\n✓ Resultados guardados en outputs/test_results.json")
 


if __name__ == "__main__":
    main()
