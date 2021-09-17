# Django Documentation in: https://docs.djangoproject.com/pt-br/2.2/ref/contrib/admin/admindocs/

app=$1
if [ "$app" == "" ]; then
    read -p "Enter Django App name: "  app
fi
if [ "$app" == "" ]; then
    app="all"
fi
file="docs/$app-$(date '+%Y%m%d-%H%M%S').png"
if [ "$app" == "all" ]; then
    app="-a"
fi
python central_data_provider/manage.py graph_models -X *CDP*,Historical*,Log*,*Session*,*User*,Group,Permission,ContentType -o $file $app
error=$?
if [ $error == 0 ]; then
    echo "Documentation created at $file"
fi
