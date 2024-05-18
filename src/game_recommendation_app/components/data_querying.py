import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


from langchain.chains import RetrievalQA

## Loading APIs
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    api_key=gemini_api_key,
    temperature=0.3,
    convert_system_message_to_human=True,
)

# Load Vector DB
new_db = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)


template = """Answer the question in your own words from the 
    context given to you.
    If questions are asked where there is no relevant context available, please answer from 
    what you know.

    Context: {context}

    Human: {question}
    Assistant:"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

memory.save_context(
    {
        "input": "Which games may you recommend for adventure lover give me 10 recommendation?, give me image url too"
    },
    {
        "output": """ Here are 10 adventure games with image URLs:

1. **Klondike Adventures**
   - Image URL: https://play-lh.googleusercontent.com/jW61KFsluyqSfGV_GhBNWdNJfmNfF8vApum1WiWw2hNR7cirY4hIaGd6fQ2zUGomRXw
   - Combines adventure, exploration, and city-building.

2. **Mythic Samkok**
   - Image URL: https://play-lh.googleusercontent.com/C4gz0QN80HKvBzoEndxCPj8FaKWYfauoztkZH4VAnDVaHjBsZUFMQGfdjQb7fejNs0d8
   - Embark on an epic journey through the Three Kingdoms.

3. **Fortias Saga: Action Adventure**
   - Image URL: https://play-lh.googleusercontent.com/-T2g7Lcbim190MJ_g7qnZmTn7zjpdrkryPeHSanFq81Je5MJUeG_0ah3KiqdesC_LeU
   - Battle monsters and recruit heroes in a nostalgic art style.

4. **Clash of Clans**
   - Image URL: https://play-lh.googleusercontent.com/LByrur1mTmPeNr0ljI-uAUcct1rzmTve5Esau1SwoAzjBXQUby6uHIfHbF9TAT51mgHm
   - Build your village, raise a clan, and compete in epic Clan Wars.

5. **Pokémon GO** (Not in provided context, but a popular choice)
   - Image URL: Search for "Pokémon GO logo" on Google Images.
   - Explore the real world to catch Pokémon.

6. **The Legend of Zelda: Breath of the Wild** (Not on Play Store, but a console/PC classic)
   - Image URL: Search for "Breath of the Wild logo" on Google Images.
   - Explore a vast open world filled with adventure and puzzles.

7. **Minecraft** (Available on Play Store)
   - Image URL: Search for "Minecraft logo" on Google Images.
   - Build, explore, and survive in a procedurally generated world.

8. **Stardew Valley** (Available on Play Store)
   - Image URL: Search for "Stardew Valley logo" on Google Images.
   - Build a farm, explore a charming town, and uncover its secrets.

9. **Terraria** (Available on Play Store)
   - Image URL: Search for "Terraria logo" on Google Images.
   - Dig, fight, explore, and build in a 2D action-adventure sandbox.

10. **Genshin Impact** (Available on Play Store)
    - Image URL: Search for "Genshin Impact logo" on Google Images.
    - Explore a vast open world with stunning visuals and engaging combat.


                 """
    },
)


retriever = new_db.as_retriever()


## Using RetrievalQA to make final query
qa = RetrievalQA.from_chain_type(
    llm=model, retriever=retriever, memory=memory, chain_type_kwargs={"prompt": prompt}
)


def my_query(query):

    result = qa.invoke({"query": query})

    return result["result"]


if __name__ == "__main__":
    res = my_query(
        "Which games may you recommend for adventure lover give me 6 recommendation?, give me image url too"
    )

    print(res)
