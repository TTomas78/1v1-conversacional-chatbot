from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
class PineconeService():
    def __init__(self, api_key, environment):
        self.index_name = "text-chat"
        self.embeddings = OpenAIEmbeddings() 
        # initialize pinecone
        pinecone.init(
            api_key=api_key,  # find at app.pinecone.io
            environment=environment  # next to api key in console
        )
        self.docsearch = Pinecone.from_existing_index(self.index_name, self.embeddings)

    def get_docsearch(self):
        return self.docsearch