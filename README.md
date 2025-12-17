# Review Responder

A simple tool to generate professional replies to customer reviews using Claude AI.

## Setup

### 1. Install dependencies
```bash
npm install
```

### 2. Set your Anthropic API key

For local development, create a `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

For Vercel deployment, add it in your project settings under Environment Variables.

### 3. Run locally
```bash
npm run dev
```

### 4. Deploy to Vercel
```bash
vercel
```

Or connect your GitHub repo to Vercel for automatic deployments.

## Structure

```
review-responder/
├── index.html      # Frontend (single file with Tailwind CDN)
├── api/
│   └── generate.js # Serverless function for Claude API
├── package.json
├── vercel.json
└── README.md
```

## Customisation

- Edit `index.html` to change the UI
- Edit `api/generate.js` to modify the prompt or model
- Tone options can be modified in both files
