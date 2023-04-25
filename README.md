# VectorDB

[![](https://dcbadge.vercel.app/api/server/aDNg6E9szy?compact=true&style=flat)](https://discord.gg/aDNg6E9szy) [![Twitter](https://img.shields.io/twitter/follow/KagiHQ?style=social)](https://twitter.com/KagiHQ) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/) 

VectorDB is a lightweight Python package for storing and retrieving text using chunking, embedding, and vector search techniques. It provides an easy-to-use interface for saving, searching, and managing textual data with associated metadata.

## Installation

To install VectorDB, use pip:

```
pip install vectordb2
```

## Usage

Here's a quick example of how to use VectorDB:

```
from vectordb import Memory

memory = Memory()

# text = "..."
# metadata = {...}

# Save text with metadata
memory.save(text, metadata)

# Search for relevant chunks
results = memory.search(query, top_n=3)
```

## Methods
Memory provides the following methods:


**__init__(self, memory_file=None, chunking_strategy={"mode":"sliding_window"},
embedding_model="sentence-transformers/all-MiniLM-L6-v2")**


- Initializes the Memory class.
- **memory_file** (str): Path to the memory file (default: None). If provided, memory will persist to disk.
- **chunking_strategy** (dict): Dictionary containing the chunking mode (default: {"mode": "sliding_window"})
   Options::
	{'mode':'sliding_window', 'window_size': 256, 'overlap': 32}
	{'mode':'paragraph'}
- **embedding_model** (str): Name of the pre-trained model to be used for embeddings (default: "sentence-transformers/all-MiniLM-L6-v2"). See [Pretrained models](https://www.sbert.net/docs/pretrained_models.html) and [MTEB](https://huggingface.co/spaces/mteb/leaderboard).

**save(self, texts, metadata_list, memory_file=None)**

- Saves the given texts and metadata to memory.
- **texts** (str or list of str): Text or list of texts to be saved.
- **metadata_list** (dict or list of dict): Metadata or list of metadata associated with the texts.
- **memory_file** (str): Path to the memory file (default: None).

**search(self, query, top_n=5)**

- Searches for the most similar chunks to the given query in memory.
- **query** (str): Query text.
- **top_n** (int): Number of most similar chunks to return (default: 5).
- Returns: List of dictionaries containing the top_n most similar chunks and their associated metadata.

**clear(self)**

- Clears the memory.


**dump(self)**

- Prints the contents of the memory.


## Example

```
from vectordb import Memory

memory = Memory(chunking_strategy={'mode':'sliding_window', 'window_size': 128, 'overlap': 16})

text = """
Machine learning is a method of data analysis that automates analytical model building.

It is a branch of artificial intelligence based on the idea that systems can learn from data,
identify patterns and make decisions with minimal human intervention.

Machine learning algorithms are trained on data sets that contain examples of the desired output. For example, a machine learning algorithm that is used to classify images might be trained on a data set that contains images of cats and dogs.
Once an algorithm is trained, it can be used to make predictions on new data. For example, the machine learning algorithm that is used to classify images could be used to predict whether a new image contains a cat or a dog.

Machine learning algorithms can be used to solve a wide variety of problems. Some common applications of machine learning include:

Classification: Categorizing data into different groups. For example, a machine learning algorithm could be used to classify emails as spam or not spam.

Regression: Predicting a continuous value. For example, a machine learning algorithm could be used to predict the price of a house.

Clustering: Finding groups of similar data points. For example, a machine learning algorithm could be used to find groups of customers with similar buying habits.

Anomaly detection: Finding data points that are different from the rest of the data. For example, a machine learning algorithm could be used to find fraudulent credit card transactions.

Machine learning is a powerful tool that can be used to solve a wide variety of problems. As the amount of data available continues to grow, machine learning is likely to become even more important in the future.

"""

metadata = {"title": "Introduction to Machine Learning", "url": "https://example.com/introduction-to-machine-learning"}

memory.save(text, metadata)

text2 = """
Artificial intelligence (AI) is the simulation of human intelligence in machines
that are programmed to think like humans and mimic their actions.

The term may also be applied to any machine that exhibits traits associated with
a human mind such as learning and problem-solving.

AI research has been highly successful in developing effective techniques for solving a wide range of problems, from game playing to medical diagnosis.

However, there is still a long way to go before AI can truly match the intelligence of humans. One of the main challenges is that human intelligence is incredibly complex and poorly understood.

Despite the challenges, AI is a rapidly growing field with the potential to revolutionize many aspects of our lives. Some of the potential benefits of AI include:

Increased productivity: AI can be used to automate tasks that are currently performed by humans, freeing up our time for more creative and fulfilling activities.

Improved decision-making: AI can be used to make more informed decisions, based on a wider range of data than humans can typically access.

Enhanced creativity: AI can be used to generate new ideas and solutions, beyond what humans can imagine on their own.
Of course, there are also potential risks associated with AI, such as:

Job displacement: As AI becomes more capable, it is possible that it will displace some human workers.

Weaponization: AI could be used to develop new weapons that are more powerful and destructive than anything we have today.

Loss of control: If AI becomes too powerful, we may lose control over it, with potentially disastrous consequences.

It is important to weigh the potential benefits and risks of AI carefully as we continue to develop this technology. With careful planning and oversight, AI has the potential to make the world a better place. However, if we are not careful, it could also lead to serious problems.
"""

metadata2 = {"title": "Introduction to Artificial Intelligence", "url": "https://example.com/introduction-to-artificial-intelligence"}

memory.save(text2, metadata2)

query = "What is the relationship between AI and machine learning?"

results = memory.search(query, top_n=3)

print(results)
```

Output:
```
[
  {
    'chunk': 'Machine learning is a method of data analysis that automates analytical model building . It is a branch of artificial intelligence based on the idea that systems can learn from data , identify patterns and make decisions with minimal human intervention . Machine learning algorithms are trained on data sets that contain examples of the desired output . For example , a machine learning algorithm that is used to classify images might be trained on a data set that contains images of cats and dogs . Once an algorithm is trained , it can be used to make predictions on new data . For example , the machine learning algorithm that is used to classify images could be used to predict whether a new image contains a cat', 
    'metadata': 
    {
      'title': 'Introduction to Machine Learning', 
      'url': 'https://example.com/introduction-to-machine-learning'
    }
  }, 
  {
    'chunk': 'Artificial intelligence ( AI ) is the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions . The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem - solving . AI research has been highly successful in developing effective techniques for solving a wide range of problems , from game playing to medical diagnosis . However , there is still a long way to go before AI can truly match the intelligence of humans . One of the main challenges is that human intelligence is incredibly complex and poorly understood . Despite the challenges , AI is a rapidly growing field with the potential to revolutionize many aspects', 
    'metadata': 
    {
      'title': 'Introduction to Artificial Intelligence', 
      'url': 'https://example.com/introduction-to-artificial-intelligence'
    }
  }, 
  {
    'chunk': 'are also potential risks associated with AI , such as : Job displacement : As AI becomes more capable , it is possible that it will displace some human workers . Weaponization : AI could be used to develop new weapons that are more powerful and destructive than anything we have today . Loss of control : If AI becomes too powerful , we may lose control over it , with potentially disastrous consequences . It is important to weigh the potential benefits and risks of AI carefully as we continue to develop this technology . With careful planning and oversight , AI has the potential to make the world a better place . However , if we are not careful , it could also lead to serious', 
    'metadata': 
    {
      'title': 'Introduction to Artificial Intelligence', 
      'url': 'https://example.com/introduction-to-artificial-intelligence'
    }
  }
]
```


## License

MIT License.
