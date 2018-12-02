class RiskAssessment:
    def __init__(self, risk):
        self._risk = risk

    @property
    def flagged(self):
        return self._risk.get('flagged')
