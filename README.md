A python3 based postfix parser that reads from txt file, parses fields and returns output in csv file.
Fields extracted are timestamp, message ID,Sender, recipient,delivery status.

#Regex compile patterns are used to identify specific parts of each line. 
#init mapping is used to setup data structures. i.e temp mapping to final structured data
#parselog fn is to read, clean and extract required fields.
#write to CSV = writes to CSV
#Main fn is for calling functions & controlling workflow
