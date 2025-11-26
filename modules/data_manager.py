import chromadb


class DataManager:

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db_storage")
        self.main_collection_name = 'articles'
        self.positivity_articles_collection_name = 'positivity_articles'
        self.negativity_articles_collection_name = 'negativity_articles'

    def get_or_create_main_collection(self):
        return self.client.get_or_create_collection(name=self.main_collection_name)

    def get_or_create_positivity_articles_collection(self):
        return self.client.get_or_create_collection(name=self.positivity_articles_collection_name)

    def get_or_create_negativity_articles_collection(self):
        return self.client.get_or_create_collection(name=self.negativity_articles_collection_name)

    def convert_article_to_point(self, article):

        point = dict()

        point['id'] = str(article.id),
        try:
            point['vector'] = article.vector.tolist()
        except AttributeError:
            point['vector'] = article.vector
        point['payload'] = {
            'title':article.title,
            'link': article.link,
            'published_time': article.published_time,
            'origin_text': article.origin_text
        }

        # for rewrite articles, after LLM processing
        if article.rewrite_text is not None:
            point['payload']['rewrite_text'] = article.rewrite_text

        return point

    def is_article_id_unique_in_main(self, article):
        id = str(article.id)

        collection = self.get_or_create_main_collection()
        result = collection.get(
            ids=[id],
            include=[]
        )
        if result and result['ids']:
            return False
        else:
            return True

    def add_article_in_main(self, article):

        collection = self.get_or_create_main_collection()
        point = self.convert_article_to_point(article)

        collection.add(
            embeddings=point['vector'],
            metadatas=point['payload'],
            ids = str(article.id)
        )

    def add_article_in_positivity_articles(self, article):

        collection = self.get_or_create_positivity_articles_collection()
        point = self.convert_article_to_point(article)

        collection.add(
            embeddings=point['vector'],
            metadatas=point['payload'],
            ids = str(article.id)
        )

    def is_article_semantics_unique_in_positivity_articles(self, article, similarity_threshold):

        collection = self.get_or_create_positivity_articles_collection()
        point = self.convert_article_to_point(article)

        results = collection.query(
            query_embeddings=point['vector'],
            n_results=1,
            include=['distances']
        ).get('distances', [[]])[0]

        if len(results) == 0 or results[0] > similarity_threshold:
            return True
        else:
            return False

    def add_article_in_negativity_articles(self, article):

        collection = self.get_or_create_negativity_articles_collection()
        point = self.convert_article_to_point(article)

        collection.add(
            embeddings=point['vector'],
            metadatas=point['payload'],
            ids = str(article.id)
        )

    def is_article_semantics_unique_in_negativity_articles(self, article, similarity_threshold):

        collection = self.get_or_create_negativity_articles_collection()
        point = self.convert_article_to_point(article)

        results = collection.query(
            query_embeddings=point['vector'],
            n_results=1,
            include=['distances']
        ).get('distances', [[]])[0]

        if len(results) == 0 or results[0] > similarity_threshold:
            return True
        else:
            return False