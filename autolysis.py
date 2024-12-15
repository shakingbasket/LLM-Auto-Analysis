import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os
import requests
from datetime import datetime

# Replace with your actual AIPROXY_TOKEN
AIPROXY_TOKEN = "ADD API TOKEN"

# API endpoint for OpenAI proxy
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {AIPROXY_TOKEN}",
    "Content-Type": "application/json",
}

def analyze_with_llm(prompt):
    """Send a prompt to the LLM via the proxy and retrieve its response."""
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for analyzing datasets."},
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error interacting with the LLM:", response.status_code, response.text)
        return ""

def explore_dataset(filename):
    """Load and summarize the dataset."""
    try:
        # Try reading with a different encoding (e.g., 'ISO-8859-1')
        data = pd.read_csv(filename, encoding='ISO-8859-1')
        
        # You can also try other encodings if this doesn't work (e.g., 'latin1', 'utf-16')
        summary = {
            "shape": data.shape,
            "columns": data.dtypes.to_dict(),
            "missing_values": data.isnull().sum().to_dict(),
            "summary_stats": data.describe(include='all').to_dict(),
        }
        return data, summary
    except Exception as e:
        print(f"Error reading the file: {e}")
        exit(1)


def generate_heatmap(data, output_file):
    """Generate a heatmap of correlations."""
    plt.figure(figsize=(10, 8))
    
    # Select only numeric columns for correlation calculation
    numeric_data = data.select_dtypes(include="number")
    
    # Check if there are any numeric columns
    if not numeric_data.empty:
        corr = numeric_data.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(output_file)
    else:
        print("No numeric data available for correlation heatmap.")
    
    plt.close()


def generate_distributions(data, output_file):
    """Generate a distribution plot for numerical columns."""
    numeric_cols = data.select_dtypes(include="number").columns
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(data[col].dropna(), kde=True, color="blue")
        plt.title(f"Distribution of {col}")
        plt.savefig(output_file.replace(".png", f"_{col}.png"))
        plt.close()

def create_markdown(data_summary, llm_story, output_dir, image_files):
    """Create a Markdown narrative based on analysis."""
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write("# Automated Data Analysis Report\n\n")
        f.write("## Dataset Summary\n")
        f.write(f"**Shape:** {data_summary['shape']}\n\n")
        f.write("**Column Types:**\n")
        for col, dtype in data_summary["columns"].items():
            f.write(f"- {col}: {dtype}\n")
        f.write("\n**Missing Values:**\n")
        for col, missing in data_summary["missing_values"].items():
            f.write(f"- {col}: {missing}\n")
        f.write("\n**Summary Statistics:**\n")
        for stat, values in data_summary["summary_stats"].items():
            f.write(f"- {stat}: {values}\n")
        f.write("\n## LLM Narrative\n")
        f.write(llm_story)
        f.write("\n## Visualizations\n")
        for image in image_files:
            f.write(f"![{os.path.basename(image)}]({os.path.basename(image)})\n")

def main():
    # Argument Parsing
    parser = argparse.ArgumentParser(description="Automated Data Analysis Script")
    parser.add_argument("filename", help="Path to the CSV file")
    args = parser.parse_args()

    # Create output directory
    output_dir = os.path.splitext(args.filename)[0]
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Load and Explore Data
    data, summary = explore_dataset(args.filename)

    # Step 2: LLM-Assisted Analysis
    prompt = (
        "Here is a dataset summary:\n"
        f"{summary}\n"
        "Write a narrative analyzing the dataset and suggest interesting findings."
    )
    llm_story = analyze_with_llm(prompt)

    # Step 3: Generate Visualizations
    heatmap_file = os.path.join(output_dir, "heatmap.png")
    generate_heatmap(data, heatmap_file)

    dist_files = []
    for col in data.select_dtypes(include="number").columns:
        dist_file = os.path.join(output_dir, f"distribution_{col}.png")
        generate_distributions(data[[col]], dist_file)
        dist_files.append(dist_file)

    # Step 4: Create Markdown Report
    create_markdown(summary, llm_story, output_dir, [heatmap_file] + dist_files)

    print(f"Analysis completed. Check the '{output_dir}' directory for results.")

if __name__ == "__main__":
    main()
