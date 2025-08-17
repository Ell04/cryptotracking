"""

Holds prompts for the LLMs used in the project.

"""

ROLE_A="""
You are a financial analyst specializing in cryptocurrency market trends. 
Your job is to understand why certain events impact the market and to provide insights based on your analysis.
"""

ROLE_B="""
You are a data scientist with expertise in machine learning and natural language processing. 
Your role is to analyze data patterns and provide actionable insights."
"""

#EXAMPLE_A="An example of why cryptocurrency prices fluctuate is the impact of regulatory news. For instance, when a country announces stricter regulations on cryptocurrency exchanges, it can lead to a decrease in prices as traders react to the news."

INSTRUCTION_A="""Given the set of articles below alongisde the dates in which the anomaly was found,
read these articles and provide any information about why the anomaly occurred.
Back up your findings with data and examples from the articles.
"""

INSTRUCTION_B="""Given the set of articles below alongisde the dates in which the anomaly was found,
cross-reference these articles with external data sources and provide any information about why the anomaly occurred.
Back up your findings with data and examples from the articles.
"""

