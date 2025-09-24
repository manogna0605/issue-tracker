import { Component, OnInit } from '@angular/core';
import { IssueService } from '../issue.service';

@Component({
  selector: 'app-issues-list',
  templateUrl: './issues-list.component.html',
  styleUrls: ['./issues-list.component.css'],
})
export class IssuesListComponent implements OnInit {
  issues = [];
  filters = { status: '', priority: '', assignee: '', page: 1, pageSize: 5 };

  constructor(private issueService: IssueService) {}

  ngOnInit(): void {
    this.loadIssues();
  }

  loadIssues() {
    this.issueService.getIssues(this.filters).subscribe((data: any) => {
      this.issues = data;
    });
  }
}