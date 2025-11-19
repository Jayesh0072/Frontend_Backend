import hashlib
import csv
import os
import json
import tempfile
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader


class PdfParser:
    def __call__(self, file):
        pdf = PdfReader(file)
        detected_text = ""

        for page in pdf.pages:
            detected_text += page.extract_text() + "\n\n"

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = text_splitter.create_documents([detected_text])
        md5_hex = hashlib.md5(detected_text.encode(encoding="UTF-8")).hexdigest()

        return documents, md5_hex


class CSVParser:
    def __call__(self, file):
        md5 = hashlib.md5()

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv") as tmp_file:
            tmp_file.write(file.getbuffer())
            loader = CSVLoader(file_path=tmp_file.name, csv_args={'delimiter': ','})
            documents = loader.load()

        for doc in documents:
            md5.update(doc.page_content.encode(encoding="UTF-8"))

        return documents, md5.hexdigest()


class VectorStore:
    LOCAL_STORAGE_INDEX_FILE = "index.json"
    PARSERS = {"pdf": PdfParser(), "csv": CSVParser()}

    def __init__(self, directory=None):
        self.vector_store = None
        self.local_storage_path = None
        self.index_file = None
        self.index = {}
        self.use_local_storage = False

        if directory is not None:
            self.use_local_storage = True
            self.local_storage_path = os.path.join(directory, "vectordb")
            self.index_file = os.path.join(self.local_storage_path, self.LOCAL_STORAGE_INDEX_FILE)
            try:
                self._load_index()
            except:
                # if we can't load the index things should still work
                pass

    def _load_index(self):
        if self.local_storage_path:
            if os.path.exists(self.index_file):
                with open(self.index_file, "r") as f:
                    self.index = json.load(f)

    def parse_file(self, file, filetype, filename):
        if filetype not in self.PARSERS:
            raise NotImplementedError("invalid filetype {}".format(filetype))

        documents, md5 = self.PARSERS.get(filetype)(file)
        vector_index = self._get_vector_index(documents, md5, filename)
        if self.vector_store is None:
            self.vector_store = vector_index
        else:
            self.vector_store.merge_from(vector_index)

    def get_vector_store(self):
        return self.vector_store

    def _get_vector_index(self, documents, md5, filename):
        if md5 in self.index:
            directory = self.index.get(md5)
            if os.path.exists(directory):
                return FAISS.load_local(directory, OpenAIEmbeddings())

        vector_index = FAISS.from_documents(documents, OpenAIEmbeddings())
        self._maybe_store_vector_index(vector_index, md5, filename)
        return vector_index

    def _maybe_store_vector_index(self, vector_index, md5, filename):
        if self.use_local_storage:
            directory = os.path.join(self.local_storage_path, os.path.splitext(filename)[0])
            vector_index.save_local(directory)
            self.index[md5] = directory
            with open(self.index_file, "w") as f:
                json.dump(self.index, f)

