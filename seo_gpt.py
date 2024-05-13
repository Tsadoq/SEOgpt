import asyncio
import logging
import time
from typing import List, Dict

from generative_model import OpenAIModel
from prompt import seo_prompt
import pandas as pd

from utils.concurrency_utils import concurrency_with_semaphores

logging.basicConfig(level=logging.INFO)


class SeoGPT:
    def __init__(self, concurrency: int = 3):
        """
        Class to generate SEO posts using OpenAI GPT model
        :param concurrency: Number of generation concurrent tasks to run
        """
        self.generative_model = OpenAIModel()
        self.seo_post_prompt = seo_prompt
        self.concurrency = concurrency

    @staticmethod
    async def generate_seo_post(
            generative_model: OpenAIModel,
            prompt: str,
            main_keyword: str,
            secondary_keywords: List[str],
    ) -> Dict[str, str]:
        """
        Generate SEO post asynchronously
        :param generative_model: OpenAIModel instance
        :param prompt: Prompt to generate answer from
        :param main_keyword: Main keyword to use for generating answer
        :param secondary_keywords: List of secondary keywords to use for generating answer
        :return: Generated answer as a dictionary with keys 'main_keyword', 'secondary_keywords', and 'response'
        """
        secondary_keywords_str = ', '.join(secondary_keywords)
        prompt = prompt.format(main_keyword=main_keyword, secondary_keywords_str=secondary_keywords_str)
        logging.info(
            f'starting generation for main keyword: {main_keyword} and secondary keywords: {secondary_keywords}')
        response = await generative_model.generate_answer_from_prompt(prompt=prompt, output_json=True)
        logging.info(
            f'Generated response for main keyword: {main_keyword} and secondary keywords: {secondary_keywords}')
        return {
            'main_keyword': main_keyword,
            'secondary_keywords': secondary_keywords,
            'response': response
        }

    async def bulk_generate_seo_posts_async(
            self,
            csv_path: str,
            main_keyword_column: str = 'Main Keyword',
            secondary_keywords_column: str = 'Secondary Keywords',
    ) -> pd.DataFrame():
        """
        Generate SEO posts from a CSV file asynchronously.
        :param csv_path: Path to the CSV file
        :param main_keyword_column: column containing the main keyword
        :param secondary_keywords_column: column containing the secondary keywords
        :return: DataFrame containing the generated SEO posts
        """
        csv_data = pd.read_csv(csv_path)
        concurrent_tasks = []
        for index, row in csv_data.iterrows():
            main_keyword = row[main_keyword_column]
            secondary_keywords = row[secondary_keywords_column].split(',')
            concurrent_tasks.append(
                self.generate_seo_post(
                    generative_model=self.generative_model,
                    prompt=self.seo_post_prompt,
                    main_keyword=main_keyword,
                    secondary_keywords=secondary_keywords
                )
            )
        results = await concurrency_with_semaphores(concurrent_tasks, num_concurrent_tasks=self.concurrency)
        return pd.DataFrame(results)

    def bulk_generate_seo_posts(
            self,
            csv_path: str,
            main_keyword_column: str = 'Main Keyword',
            secondary_keywords_column: str = 'Secondary Keywords',
    ) -> pd.DataFrame:
        """
        Generate SEO posts from a CSV file synchronously.
        :param csv_path: Path to the CSV file
        :param main_keyword_column: column containing the main keyword
        :param secondary_keywords_column: column containing the secondary keywords
        :return: DataFrame containing the generated SEO posts
        """
        return asyncio.run(
            self.bulk_generate_seo_posts_async(
                csv_path,
                main_keyword_column,
                secondary_keywords_column,
            )
        )


if __name__ == '__main__':
    concurrent_task_timing = []
    for concurrent_tasks in [1, 3, 6]:
        print(f'Generating SEO posts with {concurrent_tasks} concurrent tasks')
        seo_gpt = SeoGPT(concurrency=concurrent_tasks)
        start = time.time()
        df = seo_gpt.bulk_generate_seo_posts(csv_path='test_assets/SEO_Article_Keywords.csv')
        end = time.time()
        concurrent_task_timing.append(
            {
                '#max_concurrent_tasks': concurrent_tasks,
                'seconds': end - start
            }
        )
        print(f'Time taken to generate SEO posts with {concurrent_tasks} concurrent tasks: {end - start:.2f} seconds')
    concurrent_time_df = pd.DataFrame(concurrent_task_timing)
    print(concurrent_time_df)
    concurrent_time_df.to_excel('concurrent_time_df.xlsx', index=False)
    df.to_excel('seo_posts.xlsx', index=False)
