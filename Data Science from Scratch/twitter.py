from twython import twython

twitter = Twython(wIoB2TZlKBB8ZWmEm8ywHk77U, YCybYvr7hAGHXTWbHCKtp9Tf2lUFeY53RlwH1wigb79oasWRk4)

# search for tweets containing the phrase "data science"
for status in twitter.search(q='"data science"')["statuses"]:
	user = status["user"]["screen_name"].encode('utf-8')
	text = status["text"].encode('utf-8')
	print user, ":", text
	