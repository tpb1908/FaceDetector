from filters.Filter import Filter


class Enrolment(Filter):

    NAME = "Enrolment"

    def __init__(self, width, height, sense, active=False):
        super(Enrolment, self).__init__(width, height, Enrolment.NAME, sense, active)

        self._images = []
        self.name = None

    def start(self): # Start recording features
        self.name = raw_input("What is your name? ")
        self.name = "person_{}".format(self.name)

        names = open("names", "a")
        names.write(self.name)
        names.close()

        self._images = []

    def done(self):  # Complete the recording of a person
        pass

    def process_frame(self, frame):
        if self.name is None:  # If we aren't recording
            return frame

        people = self._sense.live_people()
        if len(people) > 1 or len(people) == 0:  # We can only deal with one person
            print "Can't enrol " + str(len(people))
        else:
            self._images.append(people[0].face().features())
            
        return frame
