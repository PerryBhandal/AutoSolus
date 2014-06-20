#How many seconds to wait between
#each course join attempt.
DELAY_BETWEEN_ATTEMPTS = 20

while true
	system("pkill firefox")
	sleep(2)
	system("python autoSolus.py")
	sleep(DELAY_BETWEEN_ATTEMPTS)
end
