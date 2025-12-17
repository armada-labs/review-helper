import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
});

export default async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { review, businessName, tone } = req.body;

    if (!review) {
        return res.status(400).json({ error: 'Review text is required' });
    }

    try {
        const message = await anthropic.messages.create({
            model: 'claude-3-haiku-20240307',
            max_tokens: 300,
            system: `You are a business owner. Write a response to a customer review.
Business Name: ${businessName || 'The Business'}
Tone: ${tone || 'Grateful'}
Rules: 
- Polite, professional, under 60 words
- No platform names like Google, Yelp, etc
- Use British English spelling and phrasing (e.g. colour, apologise, centre, whilst)
Return ONLY the reply text, nothing else.`,
            messages: [{ role: 'user', content: review }]
        });

        const reply = message.content[0].text;
        return res.status(200).json({ reply });

    } catch (error) {
        console.error('Anthropic API error:', error);
        return res.status(500).json({ error: 'Failed to generate reply' });
    }
}
