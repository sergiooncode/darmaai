class SummarizationLLMSetupException(Exception):
    def __init__(self, message=None):
        self.message = message
        super(Exception, self).__init__(message)
