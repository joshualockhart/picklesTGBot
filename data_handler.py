import pandas as pd

class Timeline():
    def __init__(self, title, events):
        self.title = title
        data = {'timestamp':[e['timestamp'] for e in events],
                'message':[e['data'] for e in events]}

        self.timeline = pd.DataFrame(data)
        self.timeline['timestamp'] = pd.to_datetime(self.timeline['timestamp'])
        self.timeline.index = self.timeline['timestamp']
        del self.timeline['timestamp']
        self.timeline.sort_index()

    def print(self):
        print(self.timeline)

    def _getEventsOnDay(self, date):
        return self.timeline[date]

    def _getHTMLDay(self, date):
        events = self._getEventsOnDay(date)
        if len(events) == 0:
            return ""
        string = "<h2>"+str(date)+"</h2>\n"

        for index, row in events.iterrows():
            string += "<em>"+str(index.time())+"</em> : "+row['message'] + "</br>\n"

        return string

    def _getHTML(self):
        string = "<html>\n<h1>" + str(self.title) + "</h1>\n"
        start_date = min(self.timeline.index)
        end_date = max(self.timeline.index)
        for date in [str(d.date()) for d in pd.date_range(start_date, end_date)]:
            string += self._getHTMLDay(date)
        string += "</html>\n"
        return string

    def _getLatexDay(self, date):
        events = self._getEventsOnDay(date)
        if len(events) == 0:
            return ""

        string = "\section*{"+str(date)+"}\n"

        for index, row in events.iterrows():
            string += "\\textbf{"+str(index.time())+"} : "+row['message'] + "\\\\ \n"

        return string

    def _getLatex(self):
        string = "\\documentclass{article}\n\\begin{document}\n"
        start_date = min(self.timeline.index)
        end_date = max(self.timeline.index)
        for date in [str(d.date()) for d in pd.date_range(start_date, end_date)]:
            string += self._getLatexDay(date)
        string += "\\end{document}\n"
        return string

    def save(self, output_filename):
        with open(output_filename,"w") as f:
            f.write(self._getLatex())

    def add_event(self, event):
        self.timeline[event.timestamp]['message'] = event.message
        self.timeline[event.timestamp]['owner_id'] = event.owner_id
        self.timeline.sort_index()
