# 🔍 AI Procurement System

An intelligent procurement system powered by CrewAI that automates the product search, comparison, and recommendation process across multiple e-commerce platforms. The system generates comprehensive procurement reports to help companies make data-driven purchasing decisions.

## 📌 Features

- 🤖 Multi-agent system using CrewAI framework
- 🔎 Intelligent search query generation
- 🌐 Multi-platform product search (Amazon, Jumia, Noon)
- 📊 Automated product data extraction and comparison
- 📑 Professional HTML procurement report generation
- 🌍 Multi-language support
- 💼 Company-specific recommendations
- 🎯 Price and value optimization
- 📈 Detailed product specifications comparison
- 🔄 Sequential workflow automation

## 📸 GUI Screenshots

### Empty Form
![Empty Form](Gui_Imgs\Img_01.png)

### Filled Form
![Filled Form](Gui_Imgs\Img_02.png)

### Running Workflow
![Running Workflow](Gui_Imgs\Img_03.png)

### Workflow Completed
![Workflow Completed](Gui_Imgs\Img_04.png)

## 📂 Project Structure

```
ai-procurement-system/
├── 🐍 Agents.py             # Agent definitions and tools
├── 📋 Tasks.py              # Task definitions and data models
├── 🖥️ gui.py                # Streamlit GUI implementation
├── 📝 requirements.txt      # Project dependencies
├── 📄 .env                  # Environment variables
├── 📁 Gui_Imgs/             # GUI image assets
│   ├── Img_01               # GUI image 1
│   ├── Img_02               # GUI image 2
│   ├── Img_03               # GUI image 3
│   └── Img_04               # GUI image 4
└── 📁 ai-agent-output/      # Output directory
    ├── step_1_suggested_search_queries.json
    ├── step_2_search_results.json
    ├── step_3_search_results.json
    └── step_4_procurement_report.html
```

## 🛠 Installation
[Previous content remains the same until Installation section]

## 🛠 Installation

### **1️⃣ Install Ollama**

1. **Install Ollama**
   - Visit the official Ollama website: https://ollama.com/
   - Download and install the appropriate version for your operating system
   - Follow the installation instructions provided on the website

2. **Install Required Model**
   - Open terminal/command prompt and run:
   ```bash
   ollama pull llama3.1:8b
   ```
   For more details, visit the [Ollama GitHub repository](https://github.com/ollama/ollama).

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**

Create a `.env` file in the project root and add:

```env
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_ORIGINS=*
OLLAMA_MODEL=ollama/llama3.1:8b
AGENTOPS_API_KEY=your_agentops_api_key
TAVILY_API_KEY=your_tavily_api_key
SGAI_API_KEY=your_sgai_api_key
output_dir=./ai-agent-output
no_keywords=10
```

## 🖥️ Running the Project

### **1. Start the Streamlit GUI**

```bash
streamlit gui.py
or
streamlit run gui.py
or
python -m streamlit gui.py
```

## 🔧 How It Works

### **CrewAI Structure**

The system utilizes four specialized AI agents working in sequence:

1. **Search Queries Recommendation Agent**: Generates targeted search queries
   - Output: `step_1_suggested_search_queries.json`
   ```json
   {
     "queries": [
       "Coffee Machine Amazon Egypt",
       "Best Coffee Machines Jumia Egypt",
       "Coffee Makers Noon Egypt En",
       ...
     ]
   }
   ```

2. **Search Engine Agent**: Performs product searches using Tavily API
   - Output: `step_2_search_results.json`
   ```json
   {
     "results": [
       {
         "title": "Product Title",
         "url": "Product URL",
         "content": "Product Description",
         "score": 0.95,
         "search_query": "Coffee Machine Amazon Egypt"
       },
       ...
     ]
   }
   ```

3. **Web Scraping Agent**: Extracts detailed product information
   - Output: `step_3_search_results.json`
   ```json
   {
     "products": [
       {
         "page_url": "Product Page URL",
         "product_title": "Product Title",
         "product_image_url": "Image URL",
         "product_current_price": 999.99,
         "product_specs": [
           {
             "specification_name": "Brand",
             "specification_value": "Example Brand"
           },
           ...
         ]
       },
       ...
     ]
   }
   ```

4. **Procurement Report Author Agent**: Generates comprehensive procurement reports
   - Output: `step_4_procurement_report.html`
   - Professional HTML report with Bootstrap styling

### **File Breakdown**

- **Agents.py**: Defines the four specialized agents and their tools
- **Tasks.py**: Contains task definitions and Pydantic data models
- **gui.py**: Implements the Streamlit-based user interface
- **.env**: Stores configuration and API keys

## 🎮 Running the Application

### **1️⃣ Start the GUI**

Launch the Streamlit interface:
```bash
streamlit run gui.py
```

### **2️⃣ Provide Inputs**

Fill in the required information:
- Company Name
- About Your Company
- Product Name
- Country Name
- Language

### **3️⃣ View Results**

After submission, the system will:
1. Generate optimal search queries (saved as ![`step_1_suggested_search_queries.json`](ai-agent-output\step_1_suggested_search_queries.json))
2. Search across specified e-commerce platforms (saved as ![`step_2_search_results.json`](ai-agent-output\step_2_search_results.json))
3. Extract detailed product information (saved as ![`step_3_search_results.json`](ai-agent-output\step_3_search_results.json))
4. Generate a comprehensive procurement report (saved as ![`step_4_procurement_report.html`](ai-agent-output\step_4_procurement_report.html))

All output files will be available in the `ai-agent-output` directory.