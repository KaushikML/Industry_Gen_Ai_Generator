import gradio as gr
from agents import (
    IndustryResearchAgent,
    MarketStandardsAgent,
    UseCaseGenerationAgent,
    ResourceAssetCollectionAgent,
    GenAISolutionsAgent,
    ReportGeneratorAgent
)

def run_workflow(company_name):
    ir = IndustryResearchAgent()
    ms = MarketStandardsAgent([
        'https://www.mckinsey.com/featured-insights/artificial-intelligence',
        'https://www2.deloitte.com/global/en/insights/technology/ai.html'
    ])
    ucg = UseCaseGenerationAgent()
    rac = ResourceAssetCollectionAgent()
    gens = GenAISolutionsAgent()
    rep = ReportGeneratorAgent()

    research = ir.run(company_name)
    trends = ms.run(research['segments'][0] if research['segments'] else research['company'])
    use_cases = ucg.run(research, trends)
    assets = rac.run(use_cases, research)
    solutions = gens.run(research)
    rep.run(use_cases, solutions, assets)

    return research['summary'], use_cases, solutions

with gr.Blocks() as demo:
    gr.Markdown("# AI/GenAI Use Case Generator")
    company_input = gr.Textbox(label="Company Name", placeholder="e.g., Tesla, Inc.")
    run_btn = gr.Button("Generate")
    summary_out = gr.Textbox(label="Company Overview")
    use_cases_out = gr.Dataframe(type="pandas", label="Use Cases")
    solutions_out = gr.Dataframe(type="pandas", label="GenAI Solutions")

    run_btn.click(
        fn=run_workflow,
        inputs=company_input,
        outputs=[summary_out, use_cases_out, solutions_out]
    )

if __name__ == '__main__':
    demo.launch()