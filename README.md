# globus


Config files for the Wits Globus Online endpoints

* `globus-map.py` goes in `/usr/local/bin`
* `gridmap` goes into `/etc/grid-security`
* `mapping.json` goes into `/opt/sysconfig/gridmap/`

## Installation steps



```


#If you don't have a project already leave --project-id out, otherwise get your project ID from your records or https://app.globus.org/settings/developers
globus-connect-server endpoint setup "za-wits-core-store03"     --organization "University of the Witwatersrand"  \
         --owner user@globusid.org --project-id $PROJECTID     --contact-email scott.hazelhurst@wits.ac.za
globus-connect-server node setup
globus-connect-server login localhost
globus-connect-server endpoint show

export ENDPOINTID=XXXXX  # from the above
export ADMINUUID=YYY # uuid of administrator
export DISKPATH=where collection goes

globus-connect-server storage-gateway create posix za-wits-core-store03-gw --domain globusid.org  --domain orcid.org --user-allow scott --identity-mapping file:/opt/sysconfig/gridmap/mapping.json

#YYYY is the uuid found from globus-connect-server show
globus-connect-server collection create $ENDPOINTID $DISKPATH --identity-id $ADMINUUID


# To allow users to connect

globus-connect-server storage-gateway  update  posix $ENDPOINTID  \
       --user-allow scott   --user-allow sandor \
       --domain globusid.org --domain orcid.org --domain wits.ac.za \
       --identity-mapping  file:/opt/sysconfig/gridmap/mapping.json

```

