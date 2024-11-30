      {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""Please write an essay with the following specifications:
                    Topic: {topic}
                    Word Count: {word_count}
                    Reference Style: {reference_style}
                    Essay Type: {essay_type}
                    Writing Style: {writing_style}
                    Tone: {tone}
                """}