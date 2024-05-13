seo_prompt = (
        "Using the main keyword '{main_keyword}' and secondary keywords '{secondary_keywords_str}', "
        "generate a structured, SEO-friendly article that is automatically tailored to the audience inferred from these keywords. "
        "The article should be 2000-2500 words. Format the output as a JSON object with an engaging article title and organized sections. "
        "Each section should include a headline and a comprehensive body text. Ensure the tone and style are suitable for the "
        "understanding level and interests of the intended audience. The text must be informative, engaging, and seamlessly integrate all keywords. "
        "Avoid keyword stuffing and maintain a logical flow throughout the article. Each section should come naturally after the previous one,"
        "\n\n---\n\n{{\"article_title\": \"...\", \"sections\": [{{\"headline\": \"...\", \"body\": \"...\"}}, {{\"headline\": \"...\", \"body\": \"...\"}}]}}"
)