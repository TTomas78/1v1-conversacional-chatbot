from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import textwrap
from profiles.templateProfile import SystemProfile,UserProfile

class AssistantService():
    def __init__(self, pinecone):
        self.system_profile = SystemProfile().data
        self.user_profile = UserProfile().data
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.pinecone = pinecone
        self.template = """
        
        Estos son mensajes de un historial de whatsapp: {docs}

        Vamos a tener una conversacion basada en el historial.

        Vas a tomar el rol de Toma Bourgeois, esto es lo que sabemos de el:
        
        {system_profile}

        El usuario es un amigo tuyo de la infancia, tienen mucha confianza y la conversacion tendra un caracter informal.

        Esto es todo lo que sabemos de el usuario:

        {user_profile}

        Deberas hablar identificando la intencionalidad del mensage del usuario y contestarle usando el mismo dialecto que toma bourgeois utiliza.

        Presta especial atencion al dialecto de Toma Bourgeois, es muy sensible a que se lo imite correctamente.

        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(self.template)

        self.prompt_messages = [system_message_prompt]

    def send_message(self,history, query, k=4):
        """
        gpt-3.5-turbo can handle up to 4097 tokens. Setting the chunksize to 1000 and k to 4 maximizes
        the number of tokens to analyze.
        """
        db = self.pinecone.get_docsearch()
        docs = db.similarity_search(query, k=k)
        docs_page_content = " ".join([d.page_content for d in docs])


        self.decode_messages(history, "-_-")
        # Template to use for the system message prompt


        human_template = "{question}"
        self.prompt_messages.append(HumanMessagePromptTemplate.from_template(human_template))


        chat_prompt = ChatPromptTemplate.from_messages(self.prompt_messages)

        chain = LLMChain(llm=self.chat, prompt=chat_prompt)

        response = chain.run(question=query, docs=docs_page_content, system_profile=self.system_profile, user_profile=self.user_profile)
        response = response.replace("\n", "").replace("¿","").replace("¡","").replace("é","e").replace("á","a").replace("í","i").replace("ó","o").replace("ú","u")
        #add the AI response to the prompt messages
        self.prompt_messages.append(SystemMessagePromptTemplate.from_template(response))
        return (textwrap.fill(response, width=50))

    def decode_messages(self,string, separator):
        index = 1
        for message in string.split(separator):
            if index % 2 == 1:
                self.prompt_messages.append(HumanMessagePromptTemplate.from_template(message))
            else:
                self.prompt_messages.append(SystemMessagePromptTemplate.from_template(message))
            index += 1