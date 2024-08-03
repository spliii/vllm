
import json

from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt

try:
    from vllm.transformers_utils.tokenizer import get_tokenizer
except ImportError:
    from backend_request_func import get_tokenizer
from transformers import PreTrainedTokenizerBase

if __name__ == "__main__":

    # dataset_path = "/data2/sp/datasets/sharegpt_gpt4.json"
    dataset_path = "/data2/sp/datasets/ShareGPT_V3_unfiltered_cleaned_split.json"
    tokenizer_id = "/data2/sp/models/Qwen2-7B-Instruct"
    tokenizer = get_tokenizer(tokenizer_id,
                              trust_remote_code=True)
    # Load the dataset.
    with open(dataset_path) as f:
        dataset = json.load(f)
    # Filter out the conversations with less than 2 turns.
    dataset = [data for data in dataset if len(data["conversations"]) >= 2]
    # dataset = [data for data in dataset if len(data["items"]) >= 2]
    
    # Only keep the first two turns of each conversation.
    dataset = [(data["conversations"][0]["value"],
                data["conversations"][1]["value"]) for data in dataset]
    # dataset = [(data["items"][0]["value"],
    #             data["items"][1]["value"]) for data in dataset]

    # Shuffle the dataset.
    # random.shuffle(dataset)

    # Filter out sequences that are too long or too short
    filtered_dataset: List[Tuple[int, int]] = []
    for i in range(len(dataset)):
        # Tokenize the prompts and completions.
        prompt = dataset[i][0]
        prompt_token_ids = tokenizer(prompt).input_ids
        completion = dataset[i][1]
        completion_token_ids = tokenizer(completion).input_ids
        prompt_len = len(prompt_token_ids)
        output_len = len(completion_token_ids)
        # if prompt_len > 1024 or prompt_len + output_len > 2048:
        #     # Prune too long sequences.
        #     continue
        filtered_dataset.append((prompt_len, output_len))

import matplotlib.pyplot as plt

def calculate_distribution(data: List[Tuple[int, int]], bins: int, ran: int) -> Tuple[List[int], List[int]]:
    """
    Calculate the distribution of lengths within the specified number of bins.
    
    Args:
        data: A list of tuples, where each tuple contains two integers representing prompt and completion lengths.
        bins: The number of bins to use for the histogram.
        
    Returns:
        Two lists containing the counts for prompts and completions respectively.
    """
    # Initialize the distribution counters
    prompt_counts = [0] * bins
    completion_counts = [0] * bins
    
    # Iterate over the data to count occurrences in each bin
    for prompt_length, completion_length in data:
        # Determine which bin the prompt length falls into
        prompt_bin = min(prompt_length // ran, bins - 1)
        prompt_counts[prompt_bin] += 1
        
        # Determine which bin the completion length falls into
        completion_bin = min(completion_length // ran, bins - 1)
        completion_counts[completion_bin] += 1
        print (prompt_counts, completion_counts)
    return prompt_counts, completion_counts


def plot_histogram(prompt_counts: List[int], completion_counts: List[int], ran: int) -> None:
    """
    Plot histograms for the distribution of prompt and completion lengths.
    
    Args:
        prompt_counts: A list of integers representing the counts of prompts per bin.
        completion_counts: A list of integers representing the counts of completions per bin.
    """
    # Define the number of bins and the bin width
    num_bins = len(prompt_counts)
    print(num_bins)
    
    # Plot the histogram for prompts
    plt.figure(figsize=(14, 7))
    plt.bar(range(num_bins), prompt_counts, width=0.8, color='blue', alpha=0.7, label='Prompts')
    plt.title('Prompt Length Distribution')
    plt.xlabel('Length')
    plt.ylabel('Count')
    plt.xticks(range(0, num_bins + 1, 5), labels=[i * ran for i in range(0, num_bins + 1, 5)])
    plt.legend()
    # plt.savefig("./output_figs/Prompt_sharegpt_4.png")
    plt.savefig("./output_figs/Prompt_sharegpt_v3.png")
    
    
    # Plot the histogram for completions
    plt.figure(figsize=(14, 7))
    plt.bar(range(num_bins), completion_counts, width=0.8, color='green', alpha=0.7, label='Completions')
    plt.title('Completion Length Distribution')
    plt.xlabel('Length')
    plt.ylabel('Count')
    plt.xticks(range(0, num_bins + 1, 5), labels=[i * ran for i in range(0, num_bins + 1, 5)])
    plt.legend()
    # plt.savefig("./output_figs/Completion_sharegpt_4.png")
    plt.savefig("./output_figs/Completion_sharegpt_v3.png")


# Assuming filtered_dataset is already defined and contains the length information
# filtered_dataset = [(prompt_length, completion_length), ...]

ran = 50

# Calculate the distribution
prompt_counts, completion_counts = calculate_distribution(filtered_dataset, 50, ran)

# Plot the histograms
plot_histogram(prompt_counts, completion_counts, ran)