class IdDates: 

    def __init__(self, identifier, start_date, end_date = None, obs = None):
        self.identifier = identifier
        self.start_date = start_date
        self.end_date = end_date
        self.obs = obs


    def update_end_date(self, end_date):
        self.end_date = end_date


    def update_obs(self, obs):
        self.obs = obs