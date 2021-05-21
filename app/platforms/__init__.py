from app.platforms.kraken import kraken

# The key is the name in the DB and the value is the module
platform_to_module = {
    kraken.platform_name: kraken
}
