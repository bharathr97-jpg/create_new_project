import streamlit as st
import requests
import pandas as pd

# Set up page configuration
st.set_page_config(
    page_title="GitHub Stats Dashboard",
    page_icon="🐙",
    layout="wide"
)

# Application Title
st.title("🐙 GitHub User Analytics Dashboard")
st.write("Enter a GitHub username below to fetch real-time profile data and repository insights.")

# Sidebar for user input
st.sidebar.header("Configuration")
username = st.sidebar.text_input("GitHub Username", value="streamlit")

if username:
    # Fetch user data from GitHub API
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url)
    
    if user_response.status_bar == 200:
        user_data = user_response.json()
        
        # Layout: Two columns for Profile Info
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(user_data['avatar_url'], width=150)
            st.subheader(user_data.get('name', username))
            st.write(f"**Bio:** {user_data.get('bio', 'No bio available')}")
            st.write(f"📍 {user_data.get('location', 'Unknown')}")
            
        with col2:
            # Metrics Row
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Public Repos", user_data['public_repos'])
            m_col2.metric("Followers", user_data['followers'])
            m_col3.metric("Following", user_data['following'])
            
        # Fetch Repositories
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        repos_response = requests.get(repos_url)
        
        if repos_response.status_code == 200:
            repos_data = repos_response.json()
            
            if repos_data:
                st.markdown("---")
                st.subheader("📊 Repository Insights")
                
                # Process data into a DataFrame
                repo_list = []
                for repo in repos_data:
                    repo_list.append({
                        "Name": repo["name"],
                        "Stars": repo["stargazers_count"],
                        "Forks": repo["forks_count"],
                        "Language": repo["language"] if repo["language"] else "Unknown",
                        "URL": repo["html_url"]
                    })
                df = pd.DataFrame(repo_list)
                
                # Chart 1: Top Repositories by Stars
                top_starred = df.sort_values(by="Stars", ascending=False).head(10)
                st.write("#### Top 10 Most Starred Repositories")
                st.bar_chart(data=top_starred, x="Name", y="Stars", color="#FF4B4B")
                
                # Chart 2: Language Distribution
                st.write("#### Primary Language Breakdown")
                lang_counts = df["Language"].value_counts().reset_index()
                lang_counts.columns = ["Language", "Count"]
                st.bar_chart(data=lang_counts, x="Language", y="Count", color="#1F77B4")
                
                # Raw Data Table
                with st.expander("📂 View All Repository Raw Data"):
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("This user has no public repositories.")
                
    elif user_response.status_code == 404:
        st.error("User not found. Please check the spelling of the GitHub username.")
else:
    st.info("Please enter a GitHub username in the sidebar to begin.")
