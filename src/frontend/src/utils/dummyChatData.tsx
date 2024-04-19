const Convo = [
    { convo_id: 1, title: "Social Media Strategy", assistant_id: 1 },
    { convo_id: 2, title: "Product Launch Preparation", assistant_id: 1 },
    { convo_id: 3, title: "Customer Retention Techniques", assistant_id: 2 },
    { convo_id: 4, title: "Website Rebranding", assistant_id: 2 },
    { convo_id: 5, title: "Online Advertising", assistant_id: 1 },
    { convo_id: 6, title: "Sales Conversion Optimization", assistant_id: 2 },
    { convo_id: 7, title: "Market Research", assistant_id: 1 },
    { convo_id: 8, title: "Email Campaign Efficiency", assistant_id: 2 },
    { convo_id: 9, title: "B2B Marketing Strategies", assistant_id: 1 },
    { convo_id: 10, title: "SEO Tactics", assistant_id: 2 },
];

const InputPrompt = [
    {
        convo_id: 1,
        author: 1,
        text_query: "Hello! Tell me about the performance of our ongoing marketing campaign.",
        file_query: null,
        response_text:
            "Ok! Let’s start with Google Ads. Your Cost Per Click (CPC) has increased by 10% this week compared to last week. The average CPC is now $1.20, up from $1.09. This could be due to increased competition for the keywords you’re targeting.",
        response_image: null,
    },
    {
        convo_id: 1,
        author: 10,
        text_query:
            "Hmm, that’s concerning. Let me know which specific campaigns or keywords are driving this increase.",
        file_query: null,
        response_text:
            "Yes, the campaigns “CloudScale Innovate” on Google Ads and “Workflow Evolution” on LinkedIn are the main contributors to this increase. The keywords “cloud management” and “CRM software” have seen a 15% and 12% increase in CPC, respectively.",
        response_image: null,
    },
    {
        convo_id: 2,
        author: 2,
        text_query: "Got it. What about our Facebook Ads? How are they performing?",
        file_query: null,
        response_text:
            "Your Facebook Ads are showing a mixed performance. The good news is that the Click-Through Rate (CTR) for the “DataHub Cloud Service” campaign has increased by 8%, now at a 2.1% CTR. However, the “DevOps Dynamics” campaign has seen a 5% decrease in CTR, now at 1.5%.",
        response_image: null,
    },
    {
        convo_id: 2,
        author: 9,
        text_query: "Critical success factors for product launch?",
        file_query: null,
        response_text: "Ensure product quality, effective marketing, and customer engagement.",
        response_image: null,
    },
    {
        convo_id: 3,
        author: 3,
        text_query: "Techniques for improving customer loyalty?",
        file_query: null,
        response_text: "Implement loyalty programs and personalized communication.",
        response_image: null,
    },
    {
        convo_id: 3,
        author: 8,
        text_query: "Best ways to handle customer complaints?",
        file_query: null,
        response_text: "Respond promptly and offer practical solutions to resolve issues.",
        response_image: null,
    },
    {
        convo_id: 4,
        author: 4,
        text_query: "Website rebranding essentials?",
        file_query: null,
        response_text: "Maintain brand consistency, focus on user experience.",
        response_image: null,
    },
    {
        convo_id: 4,
        author: 7,
        text_query: "How to measure rebranding success?",
        file_query: null,
        response_text: "Track website traffic, user engagement, and customer feedback.",
        response_image: null,
    },
    {
        convo_id: 5,
        author: 5,
        text_query: "Best platforms for online ads?",
        file_query: null,
        response_text: "Google Ads and Facebook Ads offer extensive reach.",
        response_image: null,
    },
    {
        convo_id: 5,
        author: 6,
        text_query: "Tips for ad content?",
        file_query: null,
        response_text: "Create compelling and visually appealing content.",
        response_image: null,
    },
];

const Assistant = [
    { id: 1, name: "Marketing Bot", description: "Focuses on all types of marketing strategies." },
    {
        id: 2,
        name: "Sales Expert",
        description: "Specializes in sales techniques and optimization processes.",
    },
];
const User = [
    { id: 1, username: "marketer_max", email: "max@example.com" },
    { id: 2, username: "product_patty", email: "patty@example.com" },
    { id: 3, username: "loyalty_lisa", email: "lisa@example.com" },
    { id: 4, username: "branding_bob", email: "bob@example.com" },
    { id: 5, username: "advertising_anna", email: "anna@example.com" },
    { id: 6, username: "creative_carl", email: "carl@example.com" },
    { id: 7, username: "data_david", email: "david@example.com" },
    { id: 8, username: "service_sophia", email: "sophia@example.com" },
    { id: 9, username: "launch_larry", email: "larry@example.com" },
    { id: 10, username: "social_susan", email: "susan@example.com" },
];
export { Convo, InputPrompt, Assistant, User };
