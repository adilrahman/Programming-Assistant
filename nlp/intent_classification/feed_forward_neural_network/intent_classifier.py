class NerualNetworkModel:
    def __init__(self,) -> None:
        '''
        description: None

        Inputs: None

        Ouputs: None

        '''
        self.pre_trained_model = self.load_pre_trained_model()

    def find_intent(command: str) -> str:
        '''
        description:
            find the intent of the command

        Inputs:
            command = "your command or query"

        Outputs:
            return intent

            `if this intent has low probability then return "not a command"`
        '''
        pass

    def load_pre_trained_model(self):
        '''
        description:
            load the pretrained model 

        Inputs: None
        Outputs : None

        '''
        pass


class TrainModel:
    def __init__(self, intents_json_file) -> None:
        '''
        description:
            None

        Inputs:
            intent_json_file = "your intent json file"

        Ouputs:
            return x_train,_train

        '''
        self.intents = intents_json_file
        self.training_data = self.load_training_data()

        self.x_train, self.y_train = self.training_data
        self.train()

    def load_training_data(self):
        '''
        description:
            it convert the json file into x_train, y_train

        Inputs:
           None

        Ouputs:
            return ( x_train, y_train )
        '''
        pass

    def train(self):
        '''
        desciption:
            it train the model using x_train and y_train and 
            save the model in pre_trained_model folder

        Inputs: None
        Outputs: None
        '''
        pass


if __name__ == "__main__":
    intents_json_file = ""
    trainmodel = TrainModel(intents_json_file=intents_json_file)
    trainmodel.train()
