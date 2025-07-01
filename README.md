# K8s-Flask-MySQL Project

A complete containerized web application built with Flask, MySQL, and Kubernetes. This project demonstrates a microservices architecture with a Flask web application connected to a MySQL database, all orchestrated with Kubernetes.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │    │   MySQL DB      │    │   Kubernetes    │
│   (Port 80)     │◄──►│   (Port 3306)   │    │   Orchestration │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
K8s-Flask-MySQL-Project/
├── database/                 # MySQL database configuration
│   ├── Dockerfile           # MySQL container configuration
│   ├── init.sql             # Database initialization script
│   └── my.cnf               # MySQL configuration file
├── flaskapp/                # Flask web application
│   ├── app.py               # Main Flask application
│   ├── Dockerfile           # Flask container configuration
│   └── requirements.txt     # Python dependencies
├── k8s/                     # Kubernetes manifests (to be added)
└── README.md               # This file
```

## 🚀 Features

- **Flask Web Application**: Simple web app that connects to MySQL database
- **MySQL Database**: Persistent database with user management
- **Docker Containers**: Containerized application components
- **Kubernetes Ready**: Designed for Kubernetes deployment
- **Health Check**: Database connectivity verification
- **User Management**: Basic user table with CRUD operations

## 🛠️ Prerequisites

Before running this project, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Kubernetes**: [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- **Minikube** (for local development): [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)

## 🐳 Running with Docker Compose

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd K8s-Flask-MySQL-Project
   ```

2. **Create a docker-compose.yml file**:
   ```yaml
   version: '3.8'
   
   services:
     db:
       build: ./database
       environment:
         MYSQL_ROOT_PASSWORD: rootpassword
         MYSQL_DATABASE: flaskdb
         MYSQL_USER: flaskuser
         MYSQL_PASSWORD: yourpassword
       ports:
         - "3306:3306"
       volumes:
         - mysql_data:/var/lib/mysql
   
     web:
       build: ./flaskapp
       ports:
         - "80:80"
       depends_on:
         - db
       environment:
         - DB_HOST=db
         - DB_PORT=3306
         - DB_USER=flaskuser
         - DB_PASSWORD=yourpassword
         - DB_NAME=flaskdb
   
   volumes:
     mysql_data:
   ```

3. **Start the services**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Open your browser and navigate to `http://localhost`
   - You should see: "Flask app is working! ✅ Users in DB: 0"

## ☸️ Running with Kubernetes

### Prerequisites
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- kubectl configured

### Deployment Steps

1. **Start Minikube** (if using locally):
   ```bash
   minikube start
   ```

2. **Create Kubernetes manifests** in the `k8s/` directory:

   **k8s/mysql-deployment.yaml**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: mysql-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: mysql
     template:
       metadata:
         labels:
           app: mysql
       spec:
         containers:
         - name: mysql
           image: mysql:8.0
           ports:
           - containerPort: 3306
           env:
           - name: MYSQL_ROOT_PASSWORD
             value: "rootpassword"
           - name: MYSQL_DATABASE
             value: "flaskdb"
           - name: MYSQL_USER
             value: "flaskuser"
           - name: MYSQL_PASSWORD
             value: "yourpassword"
           volumeMounts:
           - name: mysql-persistent-storage
             mountPath: /var/lib/mysql
         volumes:
         - name: mysql-persistent-storage
           persistentVolumeClaim:
             claimName: mysql-pvc
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: db-service
   spec:
     selector:
       app: mysql
     ports:
     - port: 3306
       targetPort: 3306
     type: ClusterIP
   ---
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: mysql-pvc
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 1Gi
   ```

   **k8s/flask-deployment.yaml**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: flask-deployment
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: flask
     template:
       metadata:
         labels:
           app: flask
       spec:
         containers:
         - name: flask
           image: flask-app:latest
           ports:
           - containerPort: 80
           env:
           - name: DB_HOST
             value: "db-service"
           - name: DB_PORT
             value: "3306"
           - name: DB_USER
             value: "flaskuser"
           - name: DB_PASSWORD
             value: "yourpassword"
           - name: DB_NAME
             value: "flaskdb"
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: flask-service
   spec:
     selector:
       app: flask
     ports:
     - port: 80
       targetPort: 80
     type: LoadBalancer
   ```

3. **Build and deploy**:
   ```bash
   # Build the Flask image
   docker build -t flask-app:latest ./flaskapp
   
   # Load image into Minikube (if using Minikube)
   minikube image load flask-app:latest
   
   # Apply Kubernetes manifests
   kubectl apply -f k8s/
   ```

4. **Access the application**:
   ```bash
   # Get the service URL
   minikube service flask-service
   ```

## 🔧 Configuration

### Database Configuration

The MySQL database is configured with the following default settings:
- **Database Name**: `flaskdb`
- **Username**: `flaskuser`
- **Password**: `yourpassword`
- **Port**: `3306`

### Flask Application Configuration

The Flask app connects to the database using these environment variables:
- `DB_HOST`: Database host (default: `db-service`)
- `DB_PORT`: Database port (default: `3306`)
- `DB_USER`: Database username (default: `flaskuser`)
- `DB_PASSWORD`: Database password (default: `yourpassword`)
- `DB_NAME`: Database name (default: `flaskdb`)

## 📊 Database Schema

The application creates a simple `users` table:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Monitoring and Debugging

### Check Application Status

1. **Docker Compose**:
   ```bash
   docker-compose ps
   docker-compose logs web
   docker-compose logs db
   ```

2. **Kubernetes**:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl logs <pod-name>
   ```

### Database Connection Test

The Flask application includes a health check endpoint (`/`) that:
- Attempts to connect to the MySQL database
- Executes a simple query to count users
- Returns the connection status

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**:
   - Ensure the database service is running
   - Check network connectivity between containers
   - Verify database credentials

2. **Port Already in Use**:
   - Change the port mappings in docker-compose.yml
   - Stop other services using the same ports

3. **Kubernetes Pod Issues**:
   - Check pod status: `kubectl describe pod <pod-name>`
   - View logs: `kubectl logs <pod-name>`
   - Verify image exists: `kubectl get images`

### Logs and Debugging

```bash
# Docker Compose logs
docker-compose logs -f

# Kubernetes logs
kubectl logs -f deployment/flask-deployment
kubectl logs -f deployment/mysql-deployment
```

## 🔒 Security Considerations

⚠️ **Important Security Notes**:

- Change default passwords in production
- Use secrets management for sensitive data
- Enable SSL/TLS for database connections
- Implement proper authentication and authorization
- Use network policies to restrict traffic
- Regularly update dependencies

## 📈 Scaling

### Horizontal Scaling

To scale the Flask application:

**Docker Compose**:
```bash
docker-compose up --scale web=3
```

**Kubernetes**:
```bash
kubectl scale deployment flask-deployment --replicas=5
```

### Database Scaling

For production environments, consider:
- Using managed database services
- Implementing database clustering
- Setting up read replicas
- Using connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the logs
3. Create an issue in the repository
4. Contact the maintainers

---

**Happy Coding! 🚀**