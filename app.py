import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os
import google.generativeai as gen_ai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
gemini_model = gen_ai.GenerativeModel("gemini-pro")

# Initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")

# Initialize SentenceTransformer model
model = SentenceTransformer('sentence-t5-base')

# Streamlit UI
st.title("YouTube Transcript Similarity Search")

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url, chunk_size=2000):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        # Divide transcript into chunks
        transcript_chunks = [transcript[i:i + chunk_size] for i in range(0, len(transcript), chunk_size)]
        return transcript_chunks
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return None

# Function to generate embeddings and update Qdrant database
def update_qdrant_embeddings(transcript_chunks):
    try:
        # Encode transcript chunks
        chunk_embeddings = [model.encode([chunk])[0] for chunk in transcript_chunks]
        # Generate IDs for each transcript chunk
        ids = [str(i) for i in range(len(transcript_chunks))]

        # Combine IDs and embeddings into points
        points = [{"id": i, "vector": chunk_embeddings[i]} for i in range(len(transcript_chunks))]

        # Update Qdrant database with new embeddings
        client.upsert(collection_name="genai-docs", vectors=chunk_embeddings, points=points)

    except Exception as e:
        st.error(f"Error occurred during Qdrant embeddings update: {str(e)}")

# Function to perform similarity search
def similar_search(query_data):
    try:
        # Encode the query chunk
        query_embedding = model.encode([query_data])[0]

        # Perform similarity search with distance metric
        search_results = client.search(
            collection_name="genai-docs",
            query_vector=query_embedding.tolist(),  # Convert to list
            limit=2,  # Retrieve top 3 similar chunks
        )

        return search_results
    except Exception as e:
        st.error(f"Error occurred during similarity search: {str(e)}")
        return None

# Get user input for YouTube video URL
youtube_video_url = st.text_input("Enter YouTube Video URL", "")

# Get user input for query data
# query_data = st.text_input("Enter Query Data", "")

# Process user input and display transcript
# if st.button("Extract Transcript"):
#     if youtube_video_url:
#         st.info("Fetching transcript... Please wait.")
#         transcript_chunks = extract_transcript_details(youtube_video_url)
#         st.write("Transcripts are extracted and stored in QdrantDB")
        # if transcript_chunks:
        #     st.subheader("Transcript Chunks:")

        #     for i, chunk in enumerate(transcript_chunks):
        #         # total_chunks = total_chunks + "\n" + "\n" + chunk
        #         st.write(f"Chunk {i + 1}: {chunk}")


            # prompt = f"{}"
            # st.info("Performing similarity search... Please wait.")
            # search_results = similar_search(query_data)  # Use the user's input as query data
            # if search_results:
            #     st.subheader("Top 3 Matching Results:")
            #     for result in search_results[:3]:  # Display only top 3 matching results
            #         st.write("Document ID:", result.id)
            #         st.write("Similarity Score:", result.score)
            #         st.write("Chunk URL:", result.payload["URL"])
            #         st.write("Chunk Data:", result.payload["data"])
            #         st.write("-------------------------------")
        #     #         st.write("-------------------------------")
        # else:
        #     st.warning("Please enter a valid YouTube video URL and query data.")

question = st.chat_input("Ask a question based on the provide URL")

if youtube_video_url and question:
    # Extract transcript chunks from the new YouTube video URL
    transcript_chunks = extract_transcript_details(youtube_video_url)
    
    # Update Qdrant embeddings with the new transcript chunks
    update_qdrant_embeddings(transcript_chunks)
    search_results = similar_search(question)  # Use the user's input as query data
    total_chunks = ""

    if search_results:
        # st.subheader("Top 3 Matching Results:")
        for result in search_results[:2]:  # Display only top 3 matching results
            # st.write("Document ID:", result.id)
            # st.write("Similarity Score:", result.score)
            # st.write("Chunk URL:", result.payload["URL"])
           # st.write("Chunk Data:", result.payload["data"])
            # st.write("-------------------------------")
            # st.write("-------------------------------")
            total_chunks = total_chunks + "\n" + "\n" + result.payload["data"]

    prompt = f"Question:{question} \n\n Data: {total_chunks} \n\n Instruction: Based on the above data If the question has answer in the Data then provide me the answer for question else reply with 'Unable to answer the Question'"
    # prompt = "HI"
    print(total_chunks )

    # gemini_model = prompt
    # Session
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = gemini_model.start_chat(history=[])

    gemini_response = st.session_state.chat_session.send_message(prompt)
    
    # Display Gemini's response
    # with st.chat_message("ai"):
    st.markdown(gemini_response.text)
        
    print(gemini_response.text)
