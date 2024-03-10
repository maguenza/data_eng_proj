# transform.py
# take extracted data and transform it

import extract
import pandas as pd

# Creating an function to be used in other python files
def return_dataframe(jsonFile): 
    '''
    take extracted json and convert to dataframe
    '''
    data = jsonFile

    #create empty lists to prep for columns 
    id = []
    name = []
    description = []
    duration_ms = []
    release_date = []

    # Extracting only the relevant bits of data from the json object   
    for d in data['items']:
        id.append(d['id']) 
        name.append(d['name'])
        description.append(d['description'])
        duration_ms.append(d['duration_ms'])
        release_date.append(d['release_date'])  
        
    # Prepare a dictionary in order to turn it into a pandas dataframe       
    episode_dict = {
        'id' : id,
        'name': name,
        'description' : description,
        'duration_ms' : duration_ms,
        'release_date': release_date
    }
    df = pd.DataFrame(episode_dict, columns = ['id','name','description','duration_ms','release_date'])

    return df

def quality_check(df):
    '''
    quality check for dataframe
    '''
    if df.empty:
        raise Exception('dataframe is empty')
    
    if pd.Series(df['id'].is_unique) is False:
        raise Exception('there are duplicate identifiers')
    
    if df.isnull().values.any():
        raise Exception('null values have been found')


if __name__ == '__main__':
    client_id = '4cb9bf88a1844329886f8ab395c9dea0'
    client_secret = 'e934c0e875434659b5efe6f4023c11dc'
    base_url = 'https://api.spotify.com/v1/shows/'
    show_id = '07SjDmKb9iliEzpNcN2xGD' #bill simmons podcast
    # extract data
    json_file = extract.get_request_results(client_id, client_secret, base_url, show_id)
    # convert json_file to dataframe
    load_df = return_dataframe(json_file)
    # quality check dataframe
    quality_check(load_df)
    #print results
    print(load_df)
