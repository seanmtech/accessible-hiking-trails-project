# Accessible Outdoor Recreation Directory

A directory of wheelchair-accessible national parks, trails, and campgrounds, built to help everyone enjoy the outdoors.

## 🚀 Project Structure

This monorepo contains:

- **`accessible-trails-web/`**: The frontend application built with [Astro](https://astro.build).
- **`data/`**: JSON data files containing park information.
- **`scripts/`**: Python scripts for fetching and processing data from the National Park Service (NPS) API.
- **`documentation/`**: Project documentation and planning files.

## 🛠️ Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- Python 3.8+
- An NPS API Key (get one [here](https://www.nps.gov/subjects/developer/get-started.htm))

### 1. Clone the repository

```bash
git clone <repository-url>
cd accessible-hiking-trails-project
```

### 2. Python Environment (Data Fetching)

Set up a virtual environment and install dependencies:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

Navigate to the web directory and install dependencies:

```bash
cd accessible-trails-web
npm install
```

## 🔄 Data Fetching Flow

The project uses a Python script to fetch data from the NPS API and save it to `data/parks.json`. The frontend imports this JSON file directly.

1.  **Set your API Key**:
    ```bash
    export NPS_API_KEY=your_api_key_here
    ```

2.  **Run the fetch script**:
    ```bash
    python scripts/fetch_nps.py
    ```
    This will update `data/parks.json` with the latest data from the NPS API, applying any manual overrides defined in `data/manual_overrides.json`.

## 💻 Build & Deploy

### Development

To run the frontend locally:

```bash
cd accessible-trails-web
npm run dev
```
Open http://localhost:4321 in your browser.

### Production Build

To build the site for production:

```bash
cd accessible-trails-web
npm run build
```
The output will be in `accessible-trails-web/dist/`.

### Deployment

The project is configured for deployment on Vercel (or any static site host).
1.  Connect your repository to Vercel.
2.  Set the **Root Directory** to `accessible-trails-web`.
3.  The build command (`npm run build`) and output directory (`dist`) should be detected automatically.

## 🤝 Contribution Guide

We welcome contributions! Here's how you can help:

1.  **Fork the repository**.
2.  **Create a branch** for your feature or fix (`git checkout -b feature/amazing-feature`).
3.  **Make your changes**.
    -   If changing data logic, ensure `scripts/fetch_nps.py` works correctly.
    -   If changing the UI, check `accessible-trails-web/` and ensure it builds.
4.  **Commit your changes** (`git commit -m 'Add some amazing feature'`).
5.  **Push to the branch** (`git push origin feature/amazing-feature`).
6.  **Open a Pull Request**.

### Data Validation
(Coming soon) We are adding a `scripts/validate_data.py` script to ensure data integrity. Please ensure your changes don't break the JSON schema in `data/park_schema.json`.
