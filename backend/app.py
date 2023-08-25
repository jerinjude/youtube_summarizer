
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.llms import Replicate
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from helper import *

app = Flask(__name__)
CORS(app)

#VICUNA = "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b"

# def extract_title(url):
#     return (url + '\n')* 500
def main(url):
    os.environ["REPLICATE_API_TOKEN"] = "r8_Q8S7aiimht1jjHCuO2dhm7dXXvdm1tg3Tlmr2"
    LLAMA = "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5"
    video_title = extract_title(url)
    url_transcript = url_parser(url)
    text = transcript_process(url_transcript)
    if text!='Transcript not found':
        llm = Replicate(
            model=LLAMA,
            input={
                "system_prompt": "",
                "temperature": 0.75,
                "max_length": 500,
                "top_p": 1,
            },
        )

        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"], chunk_size=20000, chunk_overlap=50
        )

        docs = text_splitter.create_documents([text])
        num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)
        if num_tokens_first_doc > 5000:
            return "Paisa adakkada naayinte mone"
        else:
            map_prompt = (
                """
            Write a concise summary of the following youtube video transcript titled """
                + video_title
                + """ :
            "{text}"
            CONCISE SUMMARY:
            """
            )

            combine_prompt = """
            Write a concise summary of the following text delimited by triple backquotes.
            Return your response as a pragraph which covers the main ideas of the text.
            Make sure the length of the summary doesn't go below 100 words.
            ```{text}```
            PARAGRAPH SUMMARY:
            """
            combine_prompt_template = PromptTemplate(
                template=combine_prompt, input_variables=["text"]
            )

            map_prompt_template = PromptTemplate(
                template=map_prompt, input_variables=["text"]
            )

            summary_chain = load_summarize_chain(
                llm=llm,
                chain_type="map_reduce",
                map_prompt=map_prompt_template,
                combine_prompt=combine_prompt_template,
                #                                      verbose=True # Set verbose=True if you want to see the prompts being used
            )
            output = summary_chain.run(docs)
            return output
    else:
        return "Sorry no transcript found!"

    
@app.route('/send-url', methods=['POST'])
def receive_url():
    data = request.get_json()
    url = data.get('url')
    
    processed_url = main(url)  # Call the extract_title function
    
    response_data = {'message': 'URL received successfully', 'processed_url': processed_url}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
