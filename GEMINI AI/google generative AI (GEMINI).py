import google.generativeai as gai
from serpapi import GoogleSearch

gai.configure(api_key='AIzaSyDCHbuLHmrFZXLIFLgptRzlnJuEdEcg37Q')

model=gai.GenerativeModel('gemini-2.0-flash')

serpapi_key = '5ea1d4f9f868c3da57b61dfe42a42e3744980e32a9c8f4b50479ce3d36cd0c48'

def google_search(query):
    param={
        'q': query,
        'hl': 'en',
        'gl': 'us',
        'api_key': serpapi_key

    }
    search = GoogleSearch(param)
    results = search.get_dict()

    if 'organic_results' in results:
        return '\n'.join([res['snippet'] for res in results['organic_results'][:5]])
    return 'no result found.'

def chat_with_gemini(query,chat_history):
    search_result = google_search(query)
    prompt = "\n".join(chat_history)
    prompt += f"\n\nUser: {query}\n(Search results: {search_result})\nAI:"
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No response from Gemini."
    except Exception as e:
        return f"Gemini error: {e}"
def s_c():

    chat_history=[]
    while True:
        user_input = input('prompt:   ')
        if user_input.lower() == 'exit':
            break
        chat_history.append(f'USer : {user_input}')  # prompt = '\n'.join(chat_history) + '\nAI'
        res = chat_with_gemini(user_input,chat_history)
        chat_history.append(f'AI : {res}')
        print(f'AI:{res}')
    print('ch')
    for i in chat_history:
        print(i)
if __name__ == "__main__":
    s_c()