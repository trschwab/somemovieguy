echo "Switching to branch master"
git checkout main

echo "Building app..."
npm run build

# Read the password from the hidden file
password=$(<.deploy_secret)

echo "Create new build location"
echo "$password" | ssh -tt troy@64.176.201.171 "sudo -S mkdir /var/www/new_build"
echo "$password" | ssh -tt troy@64.176.201.171 "sudo -S chmod -R 777 /var/www/new_build"

echo "Deploying files to server..."
scp -r build/* troy@64.176.201.171:/var/www/new_build/

# These steps for some reason don't always work properly
# Excluding for now since it takes so long to scp the build, rm on that file and doing it a second time is too
# long
# echo "Delete current production build"
# echo "$password" | ssh -tt troy@64.176.201.171 "sudo -S rm -r troyschwab.com"

# echo "Rename new build to production level"
# echo "$password" | ssh -tt troy@64.176.201.171 "sudo -S mv /var/www/new_build /var/www/troyschwab.com"

echo "Done!"