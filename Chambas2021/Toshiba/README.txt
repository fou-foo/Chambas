Round 2: PAS Technical Discussion

Please treat these data samples as confidential and do not share the data or findings outside of this interview process.

Objective:
Below are 3 datasets that represent some of the data that is collected and analyzed within the PAS that you would interact with daily.
During this next round, assume that you are a data scientist on the PAS team and be prepared to:
o	Discuss how you would use these data sources
o	Quality of data and techniques to improve or acquire additional data
o	Pseudo code and algorithms that could be used to model this
o	Any findings and conclusions within this sample data set
o	Visualization, communication, and presentation techniques for delivering insights derived from this data beyond the data science team to a customer.

Dataset 1- (DeviceTelemetry.csv):
Description: This is time series temperature sensor data for a single device in a store. High temperature can cause problems and lead to service tickets in the future.
How could you detect if and when problems occur and on which device? Is there a bad device present? If so, when did the problem occur?

Dataset 2- (SampleABC123.csv):
Description: ABC123 events are periodically sent from the host device. These events are monitored and could lead to an advanced replacement if they exceed a threshold. Excessive growth can indicate a software or hardware configuration issue.
Detect if any devices have exceeded 100%. Are any clubs and lanes experiencing problems? Also, if any devices experience a higher than usual day to day change (for example: 2%+). Hint: unique data hex field contains encoded ascii data (Unique Data: 53534420433a203134312500000000000000 = ‘SSD C: 141%’). How can this data be visualized? How can the growth be modeled to detect if certain devices are experiencing higher than normal wear / usage?

Dataset 3- (serviceTicket1day.csv):
Description: Service tickets of technicians deployed to a store for an on-site repair. 
Did any of the events from the data sources above correlate with a service ticket? What type of information can be extracted from the service data? What data quality issues exist with this type of data and what are ways to overcome them?


During this interview process, we are interested in observing how you tackle the problems and questions listed. This is a very small subset of actual data which may / may not have actual findings. We are interested in the type of conclusion that you could make from this information and how you would go about using, modelling and delivering the results. 
