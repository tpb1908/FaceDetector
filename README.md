# FaceDetector

## TODO

### UI

Main UI with buttons to each program
List of currently enrolled users
Buttons for enrolment and training etc


### Fixes

Set up the close buttons for each view


### Optimisation

Use one instance of cv2 ?? 

### Face tracking

One a person has been enrolled they can be matched
the match allow each face position on screen to be cached 
to a map (dictionary).

On each iteration the positions must then be compared to track
the movement of each face.

main loop {
    detect each face on screen
    for face in faces {
        if face can be matched to name {
            check if their is previous position in map {
                compare the position in the map and the current position
            } else {
                add face position and name to map
            }
        } else {
            generate new name 
            train
            add face position and name to map
        }
    }
}

