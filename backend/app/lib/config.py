import os


class Config(object):
    def __init__(self):
        self.data_folder = 'app/data'

        # self.knowledge_folder = os.path.join(self.data_folder, 'knowledge')
        # self.food_json = os.path.join(self.knowledge_folder, 'food.json')
        # self.pollutant_json = os.path.join(self.knowledge_folder, 'pollutant.json')
        # self.population_json = os.path.join(self.knowledge_folder, 'population.json')

        self.event_folder = os.path.join(self.data_folder, 'event')
        self.event_all = os.path.join(self.event_folder, 'comment_data_unlabeled.json')
        self.event_update = os.path.join(self.event_folder, 'newComment.json')
        self.event_labeled_file_name = 'comment_data_labeled.json'
        self.event_labeled = os.path.join(self.event_folder, self.event_labeled_file_name)

        # self.contribution_json = os.path.join(self.data_folder, 'contribution.json')

        # self.upload_folder = os.path.join(self.data_folder, 'upload')

        # os.makedirs(self.knowledge_folder, exist_ok=True)
        os.makedirs(self.event_folder, exist_ok=True)
        # os.makedirs(self.upload_folder, exist_ok=True)


CONFIG = Config()
