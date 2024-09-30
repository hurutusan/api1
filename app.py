from flask import Flask, render_template
import aiohttp
import asyncio

app = Flask(__name__)

async def fetch_curators(studio_id):
    async with aiohttp.ClientSession() as session:
        curators = []
        offset = 0
        
        while True:
            async with session.get(f"https://api.scratch.mit.edu/studios/{studio_id}/curators?offset={offset}") as response:
                if response.status != 200:
                    print("Error fetching curators:", response.status)
                    break
                
                new_curators = await response.json()
                if not new_curators:
                    break
                
                curators.extend(new_curators)
                offset += len(new_curators)
        
        return curators

async def fetch_projects(studio_id):
    async with aiohttp.ClientSession() as session:
        projects = []
        offset = 0
        limit = 30
        
        while True:
            async with session.get(f"https://api.scratch.mit.edu/studios/{studio_id}/projects?offset={offset}&limit={limit}") as response:
                if response.status != 200:
                    print("Error fetching projects:", response.status)
                    break
                
                data = await response.json()
                projects.extend(data)
                if len(data) < limit:
                    break
                
                offset += limit
        
        return projects

async def get_data(studio_id):
    curators, projects = await asyncio.gather(
        fetch_curators(studio_id),
        fetch_projects(studio_id)
    )
    return curators, projects

@app.route('/')
def index():
    studio_id = "35642753"
    curators, projects = asyncio.run(get_data(studio_id))
    return render_template('index.html', curators_count=len(curators), projects_count=len(projects))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
