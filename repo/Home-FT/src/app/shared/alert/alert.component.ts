import {Component, Input} from '@angular/core';
import {AlertType} from '../../model/alert/alert-type';
import {NgClass} from '@angular/common';

@Component({
  selector: 'app-alert',
  imports: [
    NgClass
  ],
  templateUrl: './alert.component.html',
  styleUrl: './alert.component.css'
})
export class AlertComponent {

  @Input()
  public outline: Boolean = false;

  @Input()
  public alertType: AlertType = "error"!

  @Input()
  public message: string | undefined = undefined!;

  protected getAlertClass(): string {
    return "alert-" + this.alertType
  }

}
