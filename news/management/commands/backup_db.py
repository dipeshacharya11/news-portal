"""
Database backup management command
Usage: python manage.py backup_db [--restore=backup_file] [--list] [--auto-cleanup]
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create, restore, and manage database backups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--restore',
            type=str,
            help='Restore from specific backup file',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all available backups',
        )
        parser.add_argument(
            '--auto-cleanup',
            action='store_true',
            help='Clean up old backups (keep last 10)',
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'sql'],
            default='json',
            help='Backup format (json or sql)',
        )
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Compress backup files',
        )

    def handle(self, *args, **options):
        # Create backups directory
        self.backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
        
        if options['list']:
            self.list_backups()
        elif options['restore']:
            self.restore_backup(options['restore'])
        elif options['auto_cleanup']:
            self.cleanup_old_backups()
        else:
            self.create_backup(options['format'], options['compress'])

    def create_backup(self, format_type='json', compress=False):
        """Create a new database backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'json':
            backup_filename = f'news_portal_backup_{timestamp}.json'
            self.create_json_backup(backup_filename, compress)
        else:
            backup_filename = f'news_portal_backup_{timestamp}.sql'
            self.create_sql_backup(backup_filename, compress)
        
        # Create backup metadata
        self.create_backup_metadata(backup_filename, format_type, compress)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Backup created: {backup_filename}')
        )

    def create_json_backup(self, filename, compress=False):
        """Create JSON format backup using Django's dumpdata"""
        backup_path = os.path.join(self.backup_dir, filename)
        
        self.stdout.write('📦 Creating JSON backup...')
        
        # Backup all data
        with open(backup_path, 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '--indent=2',
                stdout=f
            )
        
        # Get file size before compression
        size = os.path.getsize(backup_path)
        self.stdout.write(f'   📊 Backup size: {self.format_size(size)}')

        if compress:
            backup_path = self.compress_file(backup_path)
            compressed_size = os.path.getsize(backup_path)
            self.stdout.write(f'   📊 Compressed size: {self.format_size(compressed_size)}')

    def create_sql_backup(self, filename, compress=False):
        """Create SQL format backup (SQLite specific)"""
        backup_path = os.path.join(self.backup_dir, filename)
        
        self.stdout.write('📦 Creating SQL backup...')
        
        # For SQLite, we can copy the database file
        db_path = settings.DATABASES['default']['NAME']
        
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            # Copy SQLite database file
            shutil.copy2(db_path, backup_path.replace('.sql', '.db'))
            
            # Also create SQL dump
            with open(backup_path, 'w') as f:
                # Use sqlite3 command to dump database
                import subprocess
                try:
                    result = subprocess.run(
                        ['sqlite3', db_path, '.dump'],
                        stdout=f,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if result.returncode != 0:
                        self.stdout.write(
                            self.style.WARNING('⚠️  SQL dump failed, using DB file copy')
                        )
                except FileNotFoundError:
                    self.stdout.write(
                        self.style.WARNING('⚠️  sqlite3 command not found, using DB file copy')
                    )
        else:
            self.stdout.write(
                self.style.ERROR('❌ SQL backup only supported for SQLite databases')
            )
            return
        
        if compress:
            self.compress_file(backup_path)

    def compress_file(self, file_path):
        """Compress backup file using gzip"""
        import gzip

        compressed_path = file_path + '.gz'

        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove original file
        os.remove(file_path)

        self.stdout.write(f'   🗜️  Compressed: {os.path.basename(compressed_path)}')
        return compressed_path

    def create_backup_metadata(self, filename, format_type, compressed):
        """Create metadata file for backup"""
        metadata = {
            'filename': filename,
            'created_at': datetime.now().isoformat(),
            'format': format_type,
            'compressed': compressed,
            'django_version': self.get_django_version(),
            'database_engine': settings.DATABASES['default']['ENGINE'],
            'news_count': self.get_news_count(),
            'categories_count': self.get_categories_count(),
            'users_count': self.get_users_count(),
        }
        
        metadata_path = os.path.join(
            self.backup_dir, 
            filename.replace('.json', '.meta').replace('.sql', '.meta')
        )
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def restore_backup(self, backup_filename):
        """Restore database from backup"""
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            raise CommandError(f'❌ Backup file not found: {backup_filename}')
        
        # Check if compressed
        if backup_filename.endswith('.gz'):
            backup_path = self.decompress_file(backup_path)
        
        self.stdout.write(f'🔄 Restoring from: {backup_filename}')
        
        # Confirm restoration
        confirm = input('⚠️  This will overwrite current data. Continue? (yes/no): ')
        if confirm.lower() != 'yes':
            self.stdout.write('❌ Restoration cancelled')
            return
        
        if backup_filename.endswith('.json') or backup_filename.endswith('.json.gz'):
            self.restore_json_backup(backup_path)
        elif backup_filename.endswith('.sql') or backup_filename.endswith('.sql.gz'):
            self.restore_sql_backup(backup_path)
        else:
            raise CommandError('❌ Unsupported backup format')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Database restored successfully')
        )

    def restore_json_backup(self, backup_path):
        """Restore from JSON backup"""
        self.stdout.write('📥 Restoring JSON backup...')
        
        # Flush current data (optional - comment out to keep existing data)
        # call_command('flush', '--noinput')
        
        # Load backup data
        call_command('loaddata', backup_path)

    def restore_sql_backup(self, backup_path):
        """Restore from SQL backup"""
        self.stdout.write('📥 Restoring SQL backup...')
        
        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            db_path = settings.DATABASES['default']['NAME']
            
            # Backup current database
            current_backup = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(db_path, current_backup)
            self.stdout.write(f'   💾 Current DB backed up to: {os.path.basename(current_backup)}')
            
            # Restore from backup
            if backup_path.endswith('.db'):
                shutil.copy2(backup_path, db_path)
            else:
                # Restore from SQL dump
                import subprocess
                with open(backup_path, 'r') as f:
                    subprocess.run(['sqlite3', db_path], stdin=f)

    def list_backups(self):
        """List all available backups"""
        self.stdout.write('📋 Available Backups:')
        self.stdout.write('=' * 60)
        
        backup_files = []
        for filename in os.listdir(self.backup_dir):
            if filename.endswith(('.json', '.sql', '.db', '.gz')):
                backup_files.append(filename)
        
        if not backup_files:
            self.stdout.write('   No backups found')
            return
        
        backup_files.sort(reverse=True)  # Newest first
        
        for filename in backup_files:
            file_path = os.path.join(self.backup_dir, filename)
            size = os.path.getsize(file_path)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # Try to load metadata
            metadata_path = file_path.replace('.json', '.meta').replace('.sql', '.meta').replace('.gz', '')
            metadata = {}
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                except:
                    pass
            
            self.stdout.write(f'📄 {filename}')
            self.stdout.write(f'   📅 Created: {modified.strftime("%Y-%m-%d %H:%M:%S")}')
            self.stdout.write(f'   📊 Size: {self.format_size(size)}')
            
            if metadata:
                self.stdout.write(f'   📰 News: {metadata.get("news_count", "N/A")}')
                self.stdout.write(f'   📂 Categories: {metadata.get("categories_count", "N/A")}')
            
            self.stdout.write('')

    def cleanup_old_backups(self, keep_count=10):
        """Clean up old backup files, keeping the most recent ones"""
        self.stdout.write(f'🧹 Cleaning up old backups (keeping last {keep_count})...')
        
        backup_files = []
        for filename in os.listdir(self.backup_dir):
            if filename.endswith(('.json', '.sql', '.db', '.gz')):
                file_path = os.path.join(self.backup_dir, filename)
                backup_files.append((filename, os.path.getmtime(file_path)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        removed_count = 0
        for filename, _ in backup_files[keep_count:]:
            file_path = os.path.join(self.backup_dir, filename)
            os.remove(file_path)
            
            # Also remove metadata file
            metadata_path = file_path.replace('.json', '.meta').replace('.sql', '.meta').replace('.gz', '')
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            
            removed_count += 1
            self.stdout.write(f'   🗑️  Removed: {filename}')
        
        if removed_count == 0:
            self.stdout.write('   ✅ No old backups to remove')
        else:
            self.stdout.write(f'   ✅ Removed {removed_count} old backup(s)')

    # Helper methods
    def decompress_file(self, compressed_path):
        """Decompress gzip file"""
        import gzip
        
        decompressed_path = compressed_path.replace('.gz', '')
        
        with gzip.open(compressed_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return decompressed_path

    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def get_django_version(self):
        """Get Django version"""
        import django
        return django.get_version()

    def get_news_count(self):
        """Get total news count"""
        try:
            from news.models import News
            return News.objects.count()
        except:
            return 0

    def get_categories_count(self):
        """Get total categories count"""
        try:
            from news.models import Category
            return Category.objects.count()
        except:
            return 0

    def get_users_count(self):
        """Get total users count"""
        try:
            from django.contrib.auth.models import User
            return User.objects.count()
        except:
            return 0
