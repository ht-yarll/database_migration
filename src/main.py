from pipelines.migration import MigrationPipeline

def main():
    pipeline = MigrationPipeline()
    pipeline.migrate()

if __name__ == "__main__":
    main()
