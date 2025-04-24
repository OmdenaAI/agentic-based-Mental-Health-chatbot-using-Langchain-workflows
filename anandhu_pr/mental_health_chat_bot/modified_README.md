# API Credentials Setup Guide

This document explains how to obtain and configure the required environment variables to run this project successfully.

## Required Environment Variables

You'll need to set up the following three environment variables:
- `MODEL=gemini/gemini-1.5-pro`
- `GEMINI_API_KEY`
- `GOOGLE_APPLICATION_CREDENTIALS`

## 1. Setting the `MODEL`

The model you'll be using is `gemini/gemini-1.5-pro`. No need to obtain this — just **set the value as shown**:

```bash
MODEL=gemini/gemini-1.5-pro
```

*This tells the application which AI model to use.*

## 2. Getting `GEMINI_API_KEY`

The `GEMINI_API_KEY` is your access key to use **Google Gemini APIs**. Follow these steps to get it:

### Steps:
1. **Go to** Google AI Studio.
2. **Sign in** with your Google Account.
3. **Create a new API key**:
   * Go to **API Keys** section in your account (or directly to Google Cloud Console → API Credentials).
   * Click **Create API Key**.
4. **Copy** the generated API Key.
5. **Set it** in your environment:

```bash
GEMINI_API_KEY=your-copied-api-key
```

### ⚡ **Important:**
* Keep this key secret.
* It allows access to your billing quota (if you exceed free usage).
* You can restrict API key usage in the Google Cloud Console (highly recommended).

## 3. Getting `GOOGLE_APPLICATION_CREDENTIALS`

This variable points to a **service account key file** (JSON format) — this is needed if you are using Google Cloud services (e.g., Storage, Vertex AI).

### Steps:
1. **Go to** Google Cloud Console.
2. **Create or select** a project.
3. **Enable necessary APIs** (e.g., Gemini API, Vertex AI API, Cloud Storage API depending on your needs).
4. **Create a Service Account**:
   * Go to **IAM & Admin → Service Accounts**.
   * Click **Create Service Account**.
   * Give it a **name** and **description**.
   * **Assign roles** like:
      * Vertex AI User
      * Storage Object Admin (if you are working with storage)
      * Any other required permissions.
5. **Create and download the key**:
   * Under the service account, go to the **Keys** tab.
   * Click **Add Key → Create new key → JSON**.
   * Download the JSON file.
6. **Set the environment variable** to the path of the JSON key file:

```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json
```

## 4. Running the Project

After setting up all the credentials, follow these steps to run the project:

### Prerequisites
Make sure you have the UV package manager installed.

### Installation
Run the following command to install dependencies:

```bash
crewai install
```

### Execution
Try running the project with:

```bash
crewai run
```

### Troubleshooting
If you encounter errors with the above command, navigate to the root folder and execute the main Python script directly:

```bash
python src/mental_health_chat_bot/main.py
```