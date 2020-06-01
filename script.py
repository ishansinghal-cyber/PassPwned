import requests
import hashlib
import sys

def make_pwned_api_check(passwordchars):
	try:
		res = requests.get("https://api.pwnedpasswords.com/range/" + passwordchars)
		if(res.status_code != 200):
			print("An Error Occured acsessing the api check the API")
		return res.text
	except Exception as e:
		print("An Error Occured acsessing the api check the API")
		print(e)

def pwned_Api_format(yourpassword):
	sha1password = hashlib.sha1(yourpassword.encode('utf-8')).hexdigest().upper()
	first_5_chars , tail = sha1password[:5],sha1password[5:]
	response = make_pwned_api_check(first_5_chars)
	return get_pass_leaksCount(response,tail)

def get_pass_leaksCount(hashes,tail):
	hashes=[line.split(":") for line in hashes.splitlines()]
	for h,count in hashes:
		if(h == tail):
			return count
	return 0

def main(args):
	for password in args:
		count = pwned_Api_format(password)
		if(count):
			print(f"{password} was found {count} times... You Should probably change your password as soon as possible")
		else:
			print(f"You can go ahead the {password} is not found")


if __name__ == "__main__":
	main(sys.argv[1:])