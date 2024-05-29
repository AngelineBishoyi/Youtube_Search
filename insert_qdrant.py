from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import uuid
import hashlib
model = SentenceTransformer('sentence-t5-base')
client = QdrantClient(url="http://localhost:6333")

data = " hello all my name is crush naak and welcome to my YouTube channel so guys yet another amazing video here we are going to create an end to endend project using Google gini pro and the project name is uh related to YouTube videos transcriber now this is an amazing project our main aim will be that we will try to just give the video YouTube link YouTube video link and then it should be able to automatically extract all the text all the transcri text from that specific videos now before I go ahead uh and start implementing this I would like to give some important credits to dendra Verma so you can see that his post was there and here you can see like what all things he has specifically implemented and uh by seeing the tutorials right uh uh where I've created a lot of Germany project Google Germany projects He has specifically used this and he has actually created this so I asked for the link so that you know I could have have made a video for you all but again uh this entire project credit goes to uh dendra Verma and but I will try to implement it completely from scratch how you can actually do the setup each and everything as we go ahead okay so uh again dendra Verma thank you very much and again his LinkedIn will be provided in the description of this particular video you can go ahead and uh you know probably contact him ask him any questions if you have okay so uh let me quickly go ahead and start this specific project so here is this particular project so first of all as usual what we are going to do is that we going to go to the terminal and create our new environment okay so in order to create our new environment I will go ahead and write Honda so I don't want to do it in Powershell so let me just go back to command prompt and this is the first step that you specifically require uh and we have done this cond create P VNV and I'm going to specifically use Python 3.10 right and I'll also give Dy so that it does not ask me any permissions with respect to the installation so till the environment is going and getting created what I'm actually going to do is that I'll go ahead and create some of the files uh like EnV I also require requirements.txt so and one more file we will try to create one is app.py okay and we'll start writing our specific code with respect to this okay now what are libraries we specifically require and all as you'll know that we are going to use this uh Google G Pro over here right so let me do one thing first of all let me go ahead and create an environment variable so for that I will copy this API key from maker. google.com and I will go ahead and paste it over here right you can also do it completely it is for free Google provides you this for free for some number of request right so here I will write Google uncore API Google uncore aior key is equal to this specific environment variable okay I'm going to set this up as an environment variable I will close this I will go ahead and activate my V EnV environment now whatever uh libraries I really need to install it will be installed in in this specific environment itself right so the V EnV environment is created and we have activated it now the next thing that we have specifically going to do is that we will go ahead and use some of the libraries that we are going to use in this project one is YouTube transcript _ API why this YouTube _ transcript _ API is used let me just go ahead and show you so YouTube uncore transcript _ API so if you probably go ahead and see this is a python API which allows you to get the transcript of subtitles from a given YouTube video it also works for automatically generated subtitles supports translation of subtitles and it does not require a headless browser like celum based Solutions too okay so just by using this specific uh libraries we can probably uh you know extract all the transcript details that we have Okay so let's do one thing let's go ahead and install this I've already installed it anyhow right uh no I not installed it so I will go ahead and install it so YouTube transcript API will be required streamlet I'm to use as a front end Google generative AI python d.v path okay so these all libraries we are going to install so let's quickly go ahead and write pip install minus r requirement. txt okay let me create the screen pip install minus r requirement. dxt so quickly let's see uh so it has not installed let me see okay it is not saved this file needs to be saved anyhow now let's go ahead and do the installation perfect so once it it gets installed we will start our coding in our app. py5 okay and for coding also just understand that what all things we specifically require over here right so till this installation basically takes place uh till then I will go ahead and write the code import streamlet as St okay I'm going to use streamlet along with this I'm also going to import uh from EnV I'm going to import load uncore Dov specifically we require this for loading our API skis uh sorry environment variables and after this I will load. EnV okay so right now it is not giving us any suggestion because still the requirements uh the libraries are getting installed right so after sometime you'll be able to see that we'll also be able to see each and every suggestions from this okay so I've uh loaded this this this in short will load all the environment variables load all the environment variables okay so this is also done then import Google dot generative AI as geni done so this is also imported I'm going to specifically use this now you can see that this entire thing is loaded let me just go ahead and save it okay perfect this looks good from EnV load. EnV this is there this is there uh let me just have a look what is the [Music] error okay so from import google. generative AI as a gen I've already done this I've also imported Streamlight EnV now from I'll also create a separate utility file let me do that in the later stage U now first thing after doing this is that I will go ahead out like basic statistical your notes should aim to offer a clear understanding of all these things please provide the YouTube video transcript I will generate the detailed notes on data science and statistics accordingly again this is like you play it right so everything is written over here and you can probably check it out right but at the end of the day I will give you a simple one and at the end of the you can try as many as you like okay so I hope altogether you loved this video you like this video I hope you able to understand things uh as we go ahead more interesting videos are going to come I'm also going to explore more videos on Lama index they are also I'm also exploring one amazing Library which will actually help you to run the local models right now in Windows it has not come in it is there in Linux and Mac I have to probably record that video in Mac itself I already have a Macbook so let's see I'll do that but uh if you like this particular video uh please do share with all your friends and this was it from my side I'll see you in the next video thank you take care bye-bye "  
URL = "https://www.youtube.com/watch?v=HFfXvfFe9F8"
chunks = [data[i:i+2000] for i in range(0, len(data), 2000)]

doc_ids = []
hashed_chunks = set()
#sentence = [data]
# Iterate over chunks
for chunk in chunks:
    chunk_hash = hashlib.md5(chunk.encode()).hexdigest()
    # Check if the hash is already in the set
    if chunk_hash not in hashed_chunks:
        # Add the hash to the set
        hashed_chunks.add(chunk_hash)
        
        # Encode chunk using SentenceTransformer
        embedding = model.encode([chunk])
        embeds = embedding[0]

        # Generate a random ID
        doc_id = str(uuid.uuid4())

        # Upsert the document into the collection
        client.upsert(
            collection_name="genai-docs",
            points=[
                models.PointStruct(
                    id=doc_id,
                    vector=embeds,
                    payload={
                        "URL": URL,
                        'data': chunk,  
                    },
                ),
            ],
        )

        # Append the document ID to the list
        doc_ids.append(doc_id)

# Print success message and document IDs
print('Successful insertion of documents into multiple chunks.')
print('Document IDs:', doc_ids)