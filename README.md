# disasterfinder

diasterfinder is a Python program for finding the most effective natural disaster to spark online interest.
This program does not advocate natural disasters, however.

## Development Environment
### System
- macOS 0.15.7
- PyCharm 2020.2.3

### Python
- Python 3.8.5
- Tensorflow 2.3.1
- numpy 1.18.5

## Specifications
All of the below are one-hot encoded before being used as Keras training & testing data.

### Season indexing
    0: Winter, months 12, 1, 2
    1: Spring, months 3, 4, 5
    2: Summer, months 6, 7, 8
    3: Fall, months 9, 10, 11
    
### Disaster type indexing
    0: Wildfire
    1: Flooding
    2: Storm
    3: Earthquake

### Region/Continent indexing
    0: Africa
    1: Americas
    2: Asia
    3: Europe
    4: Oceania

### Search interest longevity
- Minimum 1 month, maximum 3 months.
- Add month when next month interest >= 0.7 * peak interest.

## Notes
`process_datasetX` reads everything from a given dataset, even when not all rows are used. Despite the slight sacrifice in performance, this makes the processing of data easier later on.
