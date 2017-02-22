from Filters.Filter import Filter

class Enrolment(Filter):

    NAME = "Enrolment"

    def __init__(self, width, height, sense, active=False):
        super(Enrolment, self).__init__(width, height, Enrolment.NAME, sense, active)
        
        self.name = None

        names = open("names", "a")
        names.write(name)
        names.close()
        # Collect and save images using cv2
        retain = 8
        w, h = 100, 100

    def start(self): # Start recording features
        self.name = raw_input("What is your name? ")
        self.name = "person_{}".format(name)
        self._images = []
    
    def done(self): # Complete the recording of a person
        pass

    def process_frame(self, frame):
        if self.name is None return frame # If we aren't recording

        people = self._sense.live_people()
        if len(people) > 1 or len(people) == 0: # We can only deal with one person
            print "Can't enrol " + str(len(people))
        else:
            self._images.append(people[0].face().features())
            
        return frame
