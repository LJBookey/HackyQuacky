import umap
import matplotlib.pyplot as plt 
import hdbscan
import batch_convert as bc
from pathlib import Path
import seaborn as sns
import shutil

def umap_reduce(specs):
    return umap.UMAP(n_components=2, n_neighbors=7).fit_transform(specs)


def plot_embeddings(embeddings):
    plt.scatter(embeddings[:, 0], embeddings[:, 1])
    plt.show()

def sort_folder_into_clusterings(chunks, labels, output_dir="data/clusterings2"):
    for i in range(len(labels)):
        cluster_path = Path(output_dir + "/" + str(labels[i]))
        if not cluster_path.exists():
            cluster_path.mkdir()
        
        shutil.copy(chunks[i].path, cluster_path)

def plot_clusterings(embeddings, labels):
    color_palette = sns.color_palette("hls", 50)
    cls_colors = [color_palette[x % 50] if x >= 0 else (0.5, 0.5, 0.5) for x in labels]
    plt.scatter(embeddings[:, 0], embeddings[:, 1], s=50, linewidth=0, c=cls_colors, alpha=1)
    plt.show()


def cluster_embeddings(embeddings, min_cluster_size=10, min_samples=2):
    clusterer = hdbscan.HDBSCAN( min_cluster_size=min_cluster_size, min_samples=min_samples)
    clusterer.fit(embeddings)
    print(max(clusterer.labels_))
    return clusterer.labels_


        
    
    

if __name__ == "__main__":
    chunks = bc.batch_load(input_dir="data/spec_chunks2", n_load=3000)
    embeddings = umap_reduce(list(chunk.spec for chunk in chunks))
    labels = cluster_embeddings(embeddings=embeddings)
    sort_folder_into_clusterings(chunks=chunks, labels=labels)
    plot_clusterings(embeddings, labels)
