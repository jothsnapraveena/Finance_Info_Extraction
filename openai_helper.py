import openai
from secret_key import openai_key
import json
import pandas as pd
openai.api_key=openai_key

def extract_financial_data(text):
    prompt=get_prompt_financial()+text
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user","content": prompt}
        ]
    )
    content=response.choices[0]['message']['content']

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(),columns=["Measure","Value"])
    except (json.JSONDecodeError,IndexError):
        pass
    return pd.DataFrame({
        "Measure":["Company Name","Stock Symbol","Revenue","Net Income","EPS"],
        "Value":["","","","",""]
    })


def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============

    '''

if __name__ == '__main__':
    text='''Tech Innovations Inc Posts Strong Q1 2024 Results

Tech Innovations Inc reported impressive financial results for the first quarter of 2024, demonstrating solid growth and profitability.

The company's revenue for Q1 2024 reached $30 million, reflecting a 15% increase compared to the same period last year. Net income for the quarter stood at $6 million, showing substantial improvement from the previous year.

Earnings per share (EPS) for the quarter came in at $0.75, up from $0.50 in Q1 2023, highlighting Tech Innovations' commitment to delivering value to its shareholders.

"We are pleased with our performance in Q1," said Jane Smith, CEO of Tech Innovations Inc. "Our focus on innovation and customer satisfaction continues to drive our success."

Investors reacted positively to the news, with Tech Innovations Inc's stock price rising by 8% in pre-market trading following the earnings release.

The company will host a conference call to discuss the results with analysts and investors later today.

    '''
    df=extract_financial_data(text)
    print(df.to_string())
