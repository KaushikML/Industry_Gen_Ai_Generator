from agents import (
    IndustryResearchAgent,
    MarketStandardsAgent,
    UseCaseGenerationAgent,
    ResourceAssetCollectionAgent,
    GenAISolutionsAgent,
    ReportGeneratorAgent
)

if __name__ == '__main__':
    company = 'Tesla, Inc.'
    ir = IndustryResearchAgent()
    ms = MarketStandardsAgent([
        'https://www.mckinsey.com/featured-insights/artificial-intelligence',
        'https://www2.deloitte.com/global/en/insights/technology/ai.html'
    ])
    uc = UseCaseGenerationAgent()
    ra = ResourceAssetCollectionAgent()
    gen = GenAISolutionsAgent()
    rep = ReportGeneratorAgent()

    research = ir.run(company)
    trends = ms.run(research['segments'][0] if research['segments'] else research['company'])
    use_cases = uc.run(research, trends)
    assets = ra.run(use_cases, research)
    solutions = gen.run(research)
    rep.run(use_cases, solutions, assets)
    print("Workflow completed. Check resources.md and Final_Proposal.md.")